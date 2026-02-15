import re
from collections import defaultdict
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd

from ..config.logger import configurar_logger
from ..services.pdf_extractor import extrair_texto_pdf
from ..utils_back.helpers import detectar_anexo, identificar_natureza_resumida

logger = configurar_logger()


class PGDASProcessor:
    def __init__(self):
        self.regex_periodo = re.compile(r"Per[ií]odo de Apura[\u00e7c][aã]o:\s*(\d{2}/\d{4})", re.IGNORECASE)
        self.regex_competencia_generica = re.compile(r"\d{2}/\d{4}")
        self.regex_cnpjs = re.compile(r"CNPJ(?:\s+\w+)? ?:?\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", re.IGNORECASE)
        self.regex_atividade = re.compile(
            r"Valor do D[\u00e9e]bito por Tributo para a Atividade \(R\$\):\s*([\s\S]*?)Receita Bruta Informada:\s*R\$\s*([\d\.,]+)",
            re.IGNORECASE,
        )
        self.regex_parcela = re.compile(
            r"Parcela \d+: R\$\s*([\d\.,]+)(.*?)\n(?=Parcela|Totais|Valor do D[\u00e9e]bito|\Z)",
            re.DOTALL | re.IGNORECASE,
        )
        self.regex_exigivel = re.compile(
            r"2\.8\)\s*Total Geral da Empresa[\s\S]*?Total do Débito Exigível\s*\(R\$\)\s*IRPJ.*?\n([\d\.,\s]+)",
            re.IGNORECASE,
        )
        self.campos_exigiveis = ["IRPJ", "CSLL", "COFINS", "PIS/Pasep", "INSS/CPP", "ICMS", "IPI", "ISS", "Total"]
        self.df_exigivel = pd.DataFrame()
        self.df_identificacao = pd.DataFrame()

    @staticmethod
    def _extrair_campo(pattern: str, texto: str) -> str:
        match = re.search(pattern, texto, re.IGNORECASE)
        if not match:
            return ""
        return match.group(1).strip()

    def separar_por_cnpj(self, texto: str) -> List[Tuple[str, str]]:
        matches = list(self.regex_cnpjs.finditer(texto))
        blocos: List[Tuple[str, str]] = []

        for i, match in enumerate(matches):
            cnpj_atual = match.group(1)
            inicio = match.start()
            fim = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
            blocos.append((cnpj_atual, texto[inicio:fim]))

        return blocos

    def processar_pdfs(self, caminhos_pdf: Iterable[str]) -> pd.DataFrame:
        todos_dados: List[Dict] = []
        todos_exigiveis: List[Dict] = []
        todos_identificacao: List[Dict] = []

        for caminho_pdf in caminhos_pdf:
            texto = extrair_texto_pdf(caminho_pdf)
            if not texto or not texto.strip():
                logger.error("PDF sem texto reconhecível", extra={"arquivo": caminho_pdf})
                continue

            competencia_dt = self._extrair_competencia(texto, caminho_pdf)

            exigivel = self.extrair_debito_exigivel(texto, competencia_dt)
            if exigivel:
                todos_exigiveis.append(exigivel)

            todos_identificacao.append(self.extrair_identificacao(texto, competencia_dt))

            for registro in self._processar_blocos_por_cnpj(texto, competencia_dt):
                todos_dados.append(registro)

        df_detalhado = pd.DataFrame(todos_dados)
        if not df_detalhado.empty and "MesAno" in df_detalhado.columns:
            df_detalhado = df_detalhado.sort_values(by="MesAno")

        self.df_exigivel = pd.DataFrame(todos_exigiveis)
        if not self.df_exigivel.empty and "MesAno" in self.df_exigivel.columns:
            self.df_exigivel = self.df_exigivel.sort_values(by="MesAno")

        self.df_identificacao = pd.DataFrame(todos_identificacao)
        if not self.df_identificacao.empty and "MesAno" in self.df_identificacao.columns:
            self.df_identificacao = self.df_identificacao.sort_values(by="MesAno")

        logger.info(
            "Processamento concluído",
            extra={
                "registros_detalhados": len(df_detalhado),
                "registros_exigiveis": len(self.df_exigivel),
                "registros_identificacao": len(self.df_identificacao),
            },
        )
        return df_detalhado

    def extrair_identificacao(self, texto: str, competencia: Optional[datetime]) -> Dict:
        return {
            "MesAno": competencia,
            "Declaração": self._extrair_campo(r"Tipo de Declaração:?\s*([^\n]+)", texto)
            or ("Retificadora" if "retificadora" in texto.lower() else "Original"),
            "CNPJ Matriz": self._extrair_campo(r"CNPJ\s+Matriz:?\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto),
            "Nome Empresarial": self._extrair_campo(r"Nome Empresarial:?\s*([^\n]+)", texto),
            "Regime de Apuração": self._extrair_campo(r"Regime de Apuração:?\s*([^\n]+)", texto),
            "Nº da Declaração": self._extrair_campo(r"N[ºo]\s*da\s*Declaração:?\s*([^\n]+)", texto),
        }

    def _extrair_competencia(self, texto: str, caminho_pdf: str) -> Optional[datetime]:
        periodo = self.regex_periodo.search(texto) or self.regex_competencia_generica.search(texto)
        if not periodo:
            logger.warning("Competência não encontrada", extra={"arquivo": caminho_pdf})
            return None

        competencia_str = periodo.group(1) if periodo.lastindex else periodo.group(0)
        try:
            return datetime.strptime(competencia_str, "%m/%Y")
        except ValueError:
            logger.warning(
                "Competência inválida no PDF",
                extra={"arquivo": caminho_pdf, "competencia": competencia_str},
            )
            return None

    def _processar_blocos_por_cnpj(self, texto: str, competencia_dt: Optional[datetime]) -> List[Dict]:
        blocos_cnpj = self.separar_por_cnpj(texto) or [("", texto)]

        grupos: Dict[str, List[str]] = defaultdict(list)
        for cnpj_valor, bloco_texto in blocos_cnpj:
            grupos[cnpj_valor].append(bloco_texto)

        registros: List[Dict] = []

        for cnpj_valor, lista_blocos in grupos.items():
            atividades_encontradas = False

            for bloco_texto in lista_blocos:
                atividades = list(self.regex_atividade.finditer(bloco_texto))
                if not atividades:
                    continue

                atividades_encontradas = True
                registros.extend(self._extrair_registros_atividades(cnpj_valor, bloco_texto, atividades, competencia_dt))

            if not atividades_encontradas and self._deve_marcar_sem_movimento(lista_blocos):
                registros.append(
                    {
                        "CNPJ": cnpj_valor,
                        "MesAno": competencia_dt,
                        "Natureza Resumida": "Sem Movimento",
                        "Anexo Aplicável": "Indeterminado",
                        "Valor": 0.0,
                        "Particularidades": "Nenhuma",
                        "Descrição Original": "Sem dados declarados",
                    }
                )

        return registros

    def _extrair_registros_atividades(
        self,
        cnpj_valor: str,
        bloco_texto: str,
        atividades: List[re.Match],
        competencia_dt: Optional[datetime],
    ) -> List[Dict]:
        registros: List[Dict] = []

        for i, atividade in enumerate(atividades):
            descricao_atividade = atividade.group(1).strip().replace("\n", " ")
            natureza = identificar_natureza_resumida(descricao_atividade)
            anexo_aplicavel = detectar_anexo(natureza)

            inicio = atividade.end()
            fim = atividades[i + 1].start() if i + 1 < len(atividades) else len(bloco_texto)
            texto_bloco = bloco_texto[inicio:fim]

            for match in self.regex_parcela.finditer(texto_bloco):
                valor = self._converter_valor(match.group(1))
                detalhes = match.group(2)

                particularidades = self.extrair_particularidades(detalhes)
                if (
                    not particularidades
                    and "sem substituição tributária/tributação monofásica/antecipação com encerramento de tributação"
                    in descricao_atividade.lower()
                ):
                    particularidades = ["Tributação normal (sem ST ou monofásica)"]

                registros.append(
                    {
                        "CNPJ": cnpj_valor,
                        "MesAno": competencia_dt,
                        "Natureza Resumida": natureza,
                        "Anexo Aplicável": anexo_aplicavel,
                        "Valor": valor,
                        "Particularidades": ", ".join(particularidades),
                        "Descrição Original": descricao_atividade,
                    }
                )

        return registros

    @staticmethod
    def _deve_marcar_sem_movimento(lista_blocos: List[str]) -> bool:
        texto_concatenado = "\n".join(lista_blocos)
        return "Receita Bruta Informada" not in texto_concatenado

    @staticmethod
    def _converter_valor(valor_raw: str) -> Optional[float]:
        try:
            return float(valor_raw.replace(".", "").replace(",", "."))
        except ValueError:
            return None

    def extrair_debito_exigivel(self, texto: str, competencia: Optional[datetime]) -> Optional[Dict]:
        match = self.regex_exigivel.search(texto)
        if not match:
            return None

        valores = match.group(1).split()
        if len(valores) < len(self.campos_exigiveis):
            logger.warning("Bloco de débito exigível incompleto", extra={"quantidade_valores": len(valores)})
            return None

        valores_float = []
        for valor in valores[: len(self.campos_exigiveis)]:
            try:
                valores_float.append(float(valor.replace(".", "").replace(",", ".")))
            except ValueError:
                valores_float.append(0.0)

        dados = {"MesAno": competencia}
        for i, campo in enumerate(self.campos_exigiveis):
            dados[campo] = valores_float[i] if i < len(valores_float) else 0.0

        return dados

    def extrair_particularidades(self, texto: str) -> List[str]:
        achadas: List[str] = []
        texto_lower = texto.lower()
        particularidades_tributos = {
            "antecipação com encerramento de tributação": ["ICMS"],
            "substituição tributária": ["ICMS", "PIS", "COFINS"],
            "tributação monofásica": ["PIS", "COFINS"],
            "exigibilidade suspensa": ["IRPJ", "CSLL", "PIS", "COFINS", "ICMS", "ISS", "IPI", "CPP"],
            "imunidade": ["ICMS", "IPI", "ISS"],
            "isenção/redução": ["ICMS", "ISS"],
            "isenção/redução cesta básica": ["ICMS"],
            "lançamento de ofício": ["IRPJ", "CSLL", "PIS", "COFINS", "ICMS", "ISS", "IPI", "CPP"],
        }

        for chave, tributos_possiveis in particularidades_tributos.items():
            if chave not in texto_lower:
                continue

            pattern = re.compile(re.escape(chave) + r"(?: de)?\s*:\s*([A-Z,\s]+)", re.IGNORECASE)
            match = pattern.search(texto)
            if match:
                tributos_encontrados = [t.strip().upper() for t in match.group(1).split(",")]
                tributos_validos = [t for t in tributos_encontrados if t in tributos_possiveis]
                if tributos_validos:
                    achadas.append(f"{chave.title()} ({', '.join(tributos_validos)})")
                    continue

            achadas.append(chave.title())

        return achadas

    def salvar_resultado(
        self,
        df: pd.DataFrame,
        df_exigivel: pd.DataFrame,
        caminho: str,
    ) -> Optional[str]:
        if df.empty and df_exigivel.empty:
            logger.warning("Nenhum dado encontrado para salvar.")
            return None

        with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:
            if not df.empty:
                df.to_excel(writer, sheet_name="segregação por atividade", index=False)
            if not df_exigivel.empty:
                df_exigivel.to_excel(writer, sheet_name="Débitos Apurados", index=False)

        logger.info("Resultado salvo", extra={"arquivo_saida": caminho})
        return caminho
