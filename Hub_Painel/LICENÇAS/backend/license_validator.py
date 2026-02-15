import base64
import datetime
import uuid
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from .license_generator import LICENSE_VERSION, LicenseError, LicenseRecord


class LicenseValidationError(LicenseError):
    """Erro de validação de licença."""


def _load_public_key(public_key_path: str):
    if not public_key_path:
        raise LicenseValidationError("Selecione a chave pública (.pem).")

    key_path = Path(public_key_path)
    if not key_path.exists():
        raise LicenseValidationError("A chave pública selecionada não foi encontrada.")

    try:
        return serialization.load_pem_public_key(key_path.read_bytes())
    except Exception as exc:
        raise LicenseValidationError(f"Não foi possível carregar a chave pública: {exc}") from exc


def _parse_license_fields(license_text: str) -> tuple[LicenseRecord, str]:
    parts = (license_text or "").strip().split("|")
    if len(parts) != 5:
        raise LicenseValidationError("Licença inválida: formato esperado v1|license_id|cliente|validade|assinatura.")

    version, license_id, client_name, expiration_raw, signature_b64 = parts

    if version != LICENSE_VERSION:
        raise LicenseValidationError(f"Versão de licença não suportada: {version}.")

    try:
        uuid.UUID(license_id)
    except ValueError as exc:
        raise LicenseValidationError("Licença inválida: license_id não é um UUID válido.") from exc

    try:
        expiration_date = datetime.date.fromisoformat(expiration_raw)
    except ValueError as exc:
        raise LicenseValidationError("Licença inválida: validade em formato inválido.") from exc

    record = LicenseRecord(
        version=version,
        license_id=license_id,
        client_name=client_name,
        expiration_date=expiration_date,
    )
    return record, signature_b64


def validate_license(license_text: str, public_key_path: str) -> LicenseRecord:
    record, signature_b64 = _parse_license_fields(license_text)
    public_key = _load_public_key(public_key_path)

    try:
        signature = base64.b64decode(signature_b64.encode(), validate=True)
    except Exception as exc:
        raise LicenseValidationError("Licença inválida: assinatura em base64 inválida.") from exc

    try:
        public_key.verify(
            signature,
            record.payload.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
    except Exception as exc:
        raise LicenseValidationError("Assinatura inválida para o conteúdo da licença.") from exc

    return record
