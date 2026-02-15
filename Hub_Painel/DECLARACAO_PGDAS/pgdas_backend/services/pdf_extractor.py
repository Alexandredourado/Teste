from pathlib import Path
from typing import Optional

import pdfplumber
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

from ..config.logger import configurar_logger

logger = configurar_logger()


def extrair_texto_pdf(caminho_pdf: str) -> Optional[str]:
    """
    Extrai texto de um PDF usando pdfplumber e PyPDF2 (fallback).
    Retorna None somente quando:
    - o arquivo não existe/não pode ser lido;
    - as duas bibliotecas falham;
    - ou o PDF não contém texto extraível.
    """
    caminho = Path(caminho_pdf)

    if not caminho.exists():
        logger.error("Arquivo PDF não encontrado", extra={"arquivo": caminho_pdf})
        return None

    texto = _extrair_com_pdfplumber(caminho)
    if texto:
        return texto

    texto = _extrair_com_pypdf2(caminho)
    if texto:
        return texto

    logger.error("Nenhuma biblioteca conseguiu extrair texto", extra={"arquivo": caminho_pdf})
    return None


def _extrair_com_pdfplumber(caminho_pdf: Path) -> Optional[str]:
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            paginas = [page.extract_text() or "" for page in pdf.pages]
            texto = "\n".join(paginas).strip()
            if texto:
                logger.info("Texto extraído com pdfplumber", extra={"arquivo": str(caminho_pdf)})
                return texto

            logger.warning("pdfplumber não encontrou texto", extra={"arquivo": str(caminho_pdf)})
            return None
    except (OSError, ValueError, TypeError) as exc:
        logger.warning(
            "Falha no pdfplumber",
            extra={"arquivo": str(caminho_pdf), "erro": str(exc)},
        )
        return None


def _extrair_com_pypdf2(caminho_pdf: Path) -> Optional[str]:
    try:
        with caminho_pdf.open("rb") as file:
            reader = PdfReader(file)
            paginas = [page.extract_text() or "" for page in reader.pages]
            texto = "\n".join(paginas).strip()
            if texto:
                logger.info("Texto extraído com PyPDF2", extra={"arquivo": str(caminho_pdf)})
                return texto

            logger.warning("PyPDF2 não encontrou texto", extra={"arquivo": str(caminho_pdf)})
            return None
    except (OSError, PdfReadError, ValueError, TypeError) as exc:
        logger.error(
            "Falha no PyPDF2",
            extra={"arquivo": str(caminho_pdf), "erro": str(exc)},
        )
        return None
