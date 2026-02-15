import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os


# ------------------------------------------------------------
#  MODELOS
# ------------------------------------------------------------
class Header0000:
    def __init__(self, empresa, cnpj, dt_inicio, dt_fim):
        self.empresa = empresa
        self.cnpj = cnpj
        self.dt_inicio = dt_inicio
        self.dt_fim = dt_fim


class RegistroH005:
    def __init__(self, dt_inv, vl_inv, mot_inv, arquivo_origem=None):
        self.dt_inv = dt_inv
        self.vl_inv = vl_inv
        self.mot_inv = mot_inv
        self.arquivo_origem = arquivo_origem


# ------------------------------------------------------------
#  PARSER DO ARQUIVO EFD
# ------------------------------------------------------------
class H005Extrator:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.header = None
        self.h005_registros = []

    def extrair(self):
        with open(self.file_path, "r", encoding="latin1") as f:
            for linha in f:
                campos = linha.strip().split("|")

                if len(campos) < 2:
                    continue

                reg = campos[1].strip().upper()

                # Registro 0000
                if reg == "0000":
                    self.header = Header0000(
                        empresa=campos[6].strip(),
                        cnpj=campos[7].strip(),
                        dt_inicio=campos[4].strip(),
                        dt_fim=campos[5].strip()
                    )

                # Registro H005
                from datetime import datetime

                if reg == "H005":
                    dt_inv = datetime.strptime(campos[2].strip(), "%d%m%Y").date()
                    vl_inv = float(campos[3].replace(".", "").replace(",", "."))

                    self.h005_registros.append(
                        RegistroH005(
                            dt_inv=dt_inv,
                            vl_inv=vl_inv,
                            mot_inv=campos[4].strip(),
                            arquivo_origem=os.path.basename(self.file_path)
                        )
                    )

        return self.header, self.h005_registros


# ------------------------------------------------------------
#  EXPORTAÇÃO PARA EXCEL
# ------------------------------------------------------------
def gerar_excel(header, registros, output_path):
    dados = []

    for reg in registros:
        dados.append({
            "CNPJ": header.cnpj,
            "EMPRESA": header.empresa,
            "DATA INVENTÁRIO": reg.dt_inv,
            "VALOR INVENTÁRIO": reg.vl_inv,
            "MOTIVO": reg.mot_inv,
            "ARQUIVO ORIGEM": reg.arquivo_origem
        })

    df = pd.DataFrame(dados)
    df.to_excel(output_path, index=False)


# ------------------------------------------------------------
#  INTERFACE – SELEÇÃO DE MÚLTIPLOS ARQUIVOS
# ------------------------------------------------------------
def selecionar_arquivos():
    caminhos = filedialog.askopenfilenames(
        title="Selecione os arquivos EFD",
        filetypes=[("Arquivo Texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    return caminhos


# ------------------------------------------------------------
#  EXECUÇÃO PRINCIPAL
# ------------------------------------------------------------
def executar_extracao():

    arquivos = selecionar_arquivos()

    if not arquivos:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
        return

    todos_registros = []
    header_primeiro = None

    for arquivo in arquivos:
        extrator = H005Extrator(arquivo)
        header, registros = extrator.extrair()

        if not header:
            messagebox.showerror("Erro", f"Registro 0000 não encontrado no arquivo:\n{arquivo}")
            continue

        # Se arquivo não tiver bloco H005 → registrar "SEM DADOS" com zeros
        if not registros:
            registros.append(
                RegistroH005(
                    dt_inv=0,                 # <<< AQUI
                    vl_inv=0,                 # <<< AQUI
                    mot_inv="SEM DADOS",      # <<< AQUI
                    arquivo_origem=os.path.basename(arquivo)
                )
            )

        if header_primeiro is None:
            header_primeiro = header

        todos_registros.extend(registros)

    if not header_primeiro or not todos_registros:
        messagebox.showerror("Erro", "Nenhum dado válido encontrado nos arquivos.")
        return

    # Salva ao lado do primeiro arquivo selecionado
    saida = os.path.join(os.path.dirname(arquivos[0]), "H005_Resultado.xlsx")

    gerar_excel(header_primeiro, todos_registros, saida)

    messagebox.showinfo(
        "Sucesso",
        f"Arquivo Excel consolidado gerado com sucesso!\n\nLocal:\n{saida}"
    )


# ------------------------------------------------------------
#  ENTRADA (APLICAÇÃO INVISÍVEL)
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    executar_extracao()
