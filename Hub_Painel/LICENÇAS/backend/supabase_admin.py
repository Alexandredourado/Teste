import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


class SupabaseConfigError(Exception):
    pass


class SupabaseRequestError(Exception):
    pass


def _parse_dotenv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    loaded: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            loaded[key] = value
    return loaded


@dataclass
class SupabaseAdminService:
    url: str
    key: str

    @classmethod
    def from_env(cls, base_dir: Path):
        url = (os.getenv("SUPABASE_URL") or "").strip().rstrip("/")
        key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY") or "").strip()

        if not (url and key):
            candidates = [
                base_dir / ".env",
                base_dir / ".env.local",
                base_dir.parent / "HUB" / ".env",
                base_dir.parent / "HUB" / ".env.local",
            ]
            for candidate in candidates:
                parsed = _parse_dotenv(candidate)
                if not parsed:
                    continue
                url = (parsed.get("SUPABASE_URL") or "").strip().rstrip("/")
                key = (parsed.get("SUPABASE_SERVICE_ROLE_KEY") or parsed.get("SUPABASE_ANON_KEY") or "").strip()
                if url and key:
                    break

        if not (url and key):
            raise SupabaseConfigError("Supabase não configurado para o módulo de licenças.")

        return cls(url=url, key=key)

    def _request(self, method: str, path: str, query: dict | None = None, body: dict | None = None, prefer: str = "return=representation"):
        query_string = "?" + urllib.parse.urlencode(query) if query else ""
        req = urllib.request.Request(
            f"{self.url}/rest/v1/{path}{query_string}",
            method=method,
            headers={
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
                "Prefer": prefer,
            },
            data=json.dumps(body).encode("utf-8") if body is not None else None,
        )
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            with opener.open(req, timeout=15) as resp:
                content = resp.read().decode("utf-8")
                return json.loads(content) if content else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise SupabaseRequestError(f"HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise SupabaseRequestError(f"Falha de conexão: {exc.reason}") from exc

    def list_modules(self):
        return self._request("GET", "modules", {"select": "module_id,module_label,is_active", "is_active": "eq.true"}) or []

    def list_licenses(self):
        return self._request("GET", "licenses", {"select": "license_id,client_name,status,expires_at,notes,metadata,created_at,updated_at", "order": "created_at.desc"}) or []

    def list_permissions(self):
        return self._request("GET", "license_module_permissions", {"select": "license_id,module_id,is_allowed"}) or []

    def create_or_update_license(self, payload: dict):
        try:
            data = self._request("POST", "licenses", {"select": "license_id,client_name,status,expires_at"}, payload)
            return data[0] if isinstance(data, list) and data else data
        except SupabaseRequestError as exc:
            if "23505" not in str(exc):
                raise
            data = self._request(
                "PATCH",
                "licenses",
                {"license_id": f"eq.{payload['license_id']}", "select": "license_id,client_name,status,expires_at"},
                {
                    "client_name": payload.get("client_name"),
                    "status": payload.get("status", "active"),
                    "expires_at": payload.get("expires_at"),
                    "updated_by": payload.get("updated_by", "gerador_licenca"),
                },
            )
            return data[0] if isinstance(data, list) and data else data

    def upsert_permission(self, license_id: str, module_id: str, is_allowed: bool):
        data = self._request(
            "POST",
            "license_module_permissions",
            {"on_conflict": "license_id,module_id", "select": "license_id,module_id,is_allowed"},
            {"license_id": license_id, "module_id": module_id, "is_allowed": bool(is_allowed)},
            prefer="resolution=merge-duplicates,return=representation",
        )
        return data[0] if isinstance(data, list) and data else data
