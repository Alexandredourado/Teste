from __future__ import annotations

from pathlib import Path
from typing import List

__all__ = [
    "alterar_linhas_icms",
    "salvar_arquivo_editado",
    "processar_arquivo",
]


# ---------------------------------------------------------------------------
# Funções de negócio
# ---------------------------------------------------------------------------

def alterar_linhas_icms(
    linhas: List[str],
    novo_cnpj: str,
    nova_ie: str,
) -> List[str]:
    """Altera CNPJ (coluna 7) e IE (coluna 10) do registro |0000|.

    Parameters
    ----------
    linhas : list[str]
        Linhas originais do arquivo TXT.
    novo_cnpj : str
        CNPJ de 14 dígitos numéricos.
    nova_ie : str
        Inscrição Estadual (tamanho variável).
    """
    if not (novo_cnpj.isdigit() and len(novo_cnpj) == 14):
        raise ValueError("CNPJ deve conter 14 dígitos numéricos")

    novas: list[str] = []
    for linha in linhas:
        if linha.startswith("|0000|"):
            campos = linha.rstrip("\n\r").split("|")
            # garante pelo menos 11 colunas (0 a 10)
            campos.extend([""] * (11 - len(campos)))
            campos[7]  = novo_cnpj  # CNPJ
            campos[10] = nova_ie    # IE
            linha = "|".join(campos) + "\n"
        novas.append(linha)
    return novas


def salvar_arquivo_editado(
    caminho_original: str | Path,
    novas_linhas: List[str],
    pasta_destino: str | Path | None = None,
) -> Path:
    """Salva ``novas_linhas`` em *pasta_destino* prefixando com EDITADO_."""
    origem = Path(caminho_original)
    destino_dir = Path(pasta_destino) if pasta_destino else origem.parent
    destino_dir.mkdir(parents=True, exist_ok=True)

    destino = destino_dir / f"EDITADO_{origem.name}"
    with destino.open("w", encoding="latin1", newline="") as f:
        f.writelines(novas_linhas)
    return destino


def processar_arquivo(
    caminho_original: str | Path,
    novo_cnpj: str,
    nova_ie: str,
    pasta_destino: str | Path | None = None,
) -> Path:
    """Altera e grava um arquivo único, retornando o novo caminho."""
    caminho_original = Path(caminho_original)
    if not caminho_original.is_file():
        raise FileNotFoundError(caminho_original)

    with caminho_original.open("r", encoding="latin1") as f:
        linhas = f.readlines()

    novas = alterar_linhas_icms(linhas, novo_cnpj, nova_ie)
    return salvar_arquivo_editado(caminho_original, novas, pasta_destino)
