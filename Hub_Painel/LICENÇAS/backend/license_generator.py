import base64
import datetime
import re
import uuid
from dataclasses import dataclass
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

LICENSE_VERSION = "v1"


class LicenseError(Exception):
    """Erro de domínio para geração/validação de licenças."""


@dataclass(frozen=True)
class LicenseRecord:
    """Representa os campos da licença antes da assinatura.

    Preparado para integração futura com backend, onde ``license_id`` será
    usado como chave de controle.
    """

    version: str
    license_id: str
    client_name: str
    expiration_date: datetime.date

    @property
    def payload(self) -> str:
        return "|".join(
            [self.version, self.license_id, self.client_name, str(self.expiration_date)]
        )


def normalize_name(nome: str) -> str:
    return (nome or "").strip().lower()


def parse_validade(data_texto: str) -> datetime.date:
    try:
        return datetime.datetime.strptime((data_texto or "").strip(), "%d/%m/%Y").date()
    except ValueError as exc:
        raise LicenseError("Data inválida. Use o formato dd/mm/aaaa.") from exc


def sanitize_filename(base_name: str) -> str:
    safe = re.sub(r"[^a-z0-9_-]+", "_", base_name.lower()).strip("_")
    return safe or "usuario"


def generate_license_id() -> str:
    return str(uuid.uuid4())


def create_license_record(nome: str, data_texto: str, *, license_id: str | None = None) -> LicenseRecord:
    nome_normalizado = normalize_name(nome)
    if not nome_normalizado:
        raise LicenseError("Informe o nome do usuário.")

    validade = parse_validade(data_texto)
    return LicenseRecord(
        version=LICENSE_VERSION,
        license_id=license_id or generate_license_id(),
        client_name=nome_normalizado,
        expiration_date=validade,
    )


def _load_private_key(private_key_path: str):
    if not private_key_path:
        raise LicenseError("Selecione a chave privada (.pem).")

    key_path = Path(private_key_path)
    if not key_path.exists():
        raise LicenseError("A chave privada selecionada não foi encontrada.")

    try:
        return serialization.load_pem_private_key(key_path.read_bytes(), password=None)
    except Exception as exc:
        raise LicenseError(f"Não foi possível carregar a chave privada: {exc}") from exc


def generate_license(nome: str, data_texto: str, private_key_path: str) -> tuple[str, str]:
    record = create_license_record(nome, data_texto)
    private_key = _load_private_key(private_key_path)

    assinatura = private_key.sign(
        record.payload.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )

    assinatura_b64 = base64.b64encode(assinatura).decode()
    licenca_final = f"{record.payload}|{assinatura_b64}"

    nome_arquivo = f"licenca_{sanitize_filename(record.client_name)}.lic"
    return nome_arquivo, licenca_final
