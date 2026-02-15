import base64
import datetime
import uuid
from dataclasses import dataclass
from pathlib import Path

LICENSE_VERSION = "v1"


class LicenseValidationError(Exception):
    """Erro de validação de licença do app final."""


@dataclass(frozen=True)
class LicenseRecord:
    version: str
    license_id: str
    client_name: str
    expiration_date: datetime.date

    @property
    def payload(self) -> str:
        return "|".join(
            [self.version, self.license_id, self.client_name, str(self.expiration_date)]
        )


def _load_public_key(public_key_path: str):
    try:
        from cryptography.hazmat.primitives import serialization
    except ModuleNotFoundError as exc:
        raise LicenseValidationError(
            "Dependência 'cryptography' não encontrada. Instale para validar licenças no app."
        ) from exc

    if not public_key_path:
        raise LicenseValidationError("Chave pública não informada.")

    key_path = Path(public_key_path)
    if not key_path.exists():
        raise LicenseValidationError(
            f"Chave pública não encontrada: {public_key_path}"
        )

    try:
        return serialization.load_pem_public_key(key_path.read_bytes())
    except Exception as exc:
        raise LicenseValidationError(f"Falha ao carregar chave pública: {exc}") from exc


def _parse_license_fields(license_text: str) -> tuple[LicenseRecord, str]:
    parts = (license_text or "").strip().split("|")
    if len(parts) != 5:
        raise LicenseValidationError(
            "Licença inválida: formato esperado v1|license_id|cliente|validade|assinatura."
        )

    version, license_id, client_name, expiration_raw, signature_b64 = parts

    if version != LICENSE_VERSION:
        raise LicenseValidationError(f"Versão de licença não suportada: {version}.")

    try:
        uuid.UUID(license_id)
    except ValueError as exc:
        raise LicenseValidationError("license_id inválido: UUID esperado.") from exc

    try:
        expiration_date = datetime.date.fromisoformat(expiration_raw)
    except ValueError as exc:
        raise LicenseValidationError("Data de validade da licença inválida.") from exc

    return (
        LicenseRecord(
            version=version,
            license_id=license_id,
            client_name=client_name,
            expiration_date=expiration_date,
        ),
        signature_b64,
    )


def validate_license_file(license_path: str, public_key_path: str) -> LicenseRecord:
    path = Path(license_path)
    if not path.exists():
        raise LicenseValidationError(
            f"Licença não encontrada: {license_path}. Gere/instale o arquivo .lic antes de abrir o app."
        )

    license_text = path.read_text(encoding="utf-8")
    record, signature_b64 = _parse_license_fields(license_text)

    try:
        signature = base64.b64decode(signature_b64.encode(), validate=True)
    except Exception as exc:
        raise LicenseValidationError("Assinatura da licença em base64 inválida.") from exc

    public_key = _load_public_key(public_key_path)

    try:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding

        public_key.verify(
            signature,
            record.payload.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
    except LicenseValidationError:
        raise
    except Exception as exc:
        raise LicenseValidationError("Assinatura da licença inválida.") from exc

    if datetime.date.today() > record.expiration_date:
        raise LicenseValidationError(
            f"Licença expirada em {record.expiration_date.isoformat()}."
        )

    return record
