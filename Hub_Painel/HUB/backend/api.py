from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .module_registry import list_areas_with_modules, list_module_catalog
from .supabase_client import SupabaseConfigError, SupabaseLicenseService, SupabaseRequestError

app = FastAPI(title="Hansu HUB API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _license_status(expires_at: str | None, status: str | None) -> str:
    if status and status.lower() in {"suspended", "suspensa"}:
        return "Suspensa"
    if not expires_at:
        return "Ativa"

    try:
        expires_dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    except ValueError:
        return "Ativa"

    now = datetime.now(timezone.utc)
    if expires_dt < now:
        return "Suspensa"

    days_left = (expires_dt - now).days
    if days_left <= 30:
        return "Expirando"
    return "Ativa"


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/modules/areas")
def modules_areas() -> list[dict]:
    return list_areas_with_modules()


@app.get("/api/modules/catalog")
def modules_catalog() -> list[dict]:
    return list_module_catalog()


@app.get("/api/licenses")
def licenses() -> list[dict]:
    try:
        service = SupabaseLicenseService.from_env()
        licenses_data = service.list_licenses() or []
    except SupabaseConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except SupabaseRequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    normalized = []
    for item in licenses_data:
        normalized.append(
            {
                "id": item.get("license_id", "N/A"),
                "cliente": item.get("client_name") or "Sem nome",
                "modulo": "Hansu Hub",
                "status": _license_status(item.get("expires_at"), item.get("status")),
                "expira": item.get("expires_at") or "Indefinida",
            }
        )

    return normalized
