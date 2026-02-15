import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path


class SupabaseConfigError(Exception):
    """Erro de configuração de integração com Supabase."""


class SupabaseRequestError(Exception):
    """Erro de comunicação com Supabase."""


def _parse_dotenv(dotenv_path: Path) -> dict[str, str]:
    loaded: dict[str, str] = {}
    if not dotenv_path.exists() or not dotenv_path.is_file():
        return loaded

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        loaded[key] = value

    return loaded


@dataclass
class SupabaseLicenseService:
    url: str
    key: str
    timeout_s: int = 15
    _opener: urllib.request.OpenerDirector = field(init=False, repr=False)

    def __post_init__(self):
        # Evita problemas com proxies do ambiente que interceptam HTTPS e
        # costumam retornar 403 em chamadas para o Supabase.
        self._opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    @classmethod
    def from_env(cls, base_dir: Path | None = None):
        env_url = (os.getenv("SUPABASE_URL") or "").strip().rstrip("/")
        env_key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY") or "").strip()
        if env_url and env_key:
            return cls(url=env_url, key=env_key)

        search_base = base_dir or Path.cwd()
        dotenv_candidates = [
            search_base / ".env",
            search_base / ".env.local",
            search_base.parent / ".env",
            search_base.parent / ".env.local",
            Path.cwd() / ".env",
        ]

        dotenv_url = ""
        dotenv_key = ""
        used_dotenv = None
        for candidate in dotenv_candidates:
            parsed = _parse_dotenv(candidate)
            if not parsed:
                continue

            current_url = (parsed.get("SUPABASE_URL") or "").strip().rstrip("/")
            current_key = (
                parsed.get("SUPABASE_SERVICE_ROLE_KEY")
                or parsed.get("SUPABASE_ANON_KEY")
                or ""
            ).strip()
            if current_url and current_key:
                dotenv_url = current_url
                dotenv_key = current_key
                used_dotenv = candidate
                break

        if dotenv_url and dotenv_key:
            return cls(url=dotenv_url, key=dotenv_key)

        tried = ", ".join(str(path) for path in dotenv_candidates)
        detail = f"Arquivos verificados: {tried}."
        if used_dotenv:
            detail = f"Arquivo lido sem chaves válidas: {used_dotenv}."

        raise SupabaseConfigError(
            "Supabase não configurado. Defina SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY "
            f"nas variáveis de ambiente ou em .env/.env.local. {detail}"
        )

    def _request(
        self,
        method: str,
        path: str,
        query: dict | None = None,
        body: dict | None = None,
        extra_headers: dict | None = None,
    ):
        query_string = ""
        if query:
            query_string = "?" + urllib.parse.urlencode(query)

        headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        if extra_headers:
            headers.update(extra_headers)

        req = urllib.request.Request(
            f"{self.url}/rest/v1/{path}{query_string}",
            method=method,
            headers=headers,
            data=json.dumps(body).encode("utf-8") if body is not None else None,
        )

        try:
            with self._opener.open(req, timeout=self.timeout_s) as response:
                content = response.read().decode("utf-8")
                return json.loads(content) if content else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise SupabaseRequestError(f"HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise SupabaseRequestError(f"Falha de conexão com Supabase: {exc.reason}") from exc

    def list_modules(self):
        return self._request(
            "GET",
            "modules",
            {
                "select": "module_id,module_label,area_id,area_label,is_active",
                "order": "area_label.asc,module_label.asc",
            },
        )

    def list_licenses(self):
        return self._request(
            "GET",
            "licenses",
            {
                "select": "license_id,client_name,status,expires_at,notes,metadata,created_at,updated_at",
                "order": "created_at.desc",
            },
        )

    def list_permissions(self):
        return self._request(
            "GET",
            "license_module_permissions",
            {
                "select": "license_id,module_id,is_allowed",
            },
        )

    def list_allowed_modules_for_license(self, license_id: str):
        """Retorna os módulos liberados para uma licença em uma única consulta."""
        return self._request(
            "GET",
            "license_module_permissions",
            {
                "select": "module_id",
                "license_id": f"eq.{license_id}",
                "is_allowed": "eq.true",
            },
        ) or []


    def create_module(self, payload: dict):
        data = self._request(
            "POST",
            "modules",
            {
                "on_conflict": "module_id",
                "select": "module_id,module_label,area_id,area_label,is_active",
            },
            body=payload,
            extra_headers={
                "Prefer": "resolution=merge-duplicates,return=representation",
            },
        )
        return data[0] if isinstance(data, list) and data else data

    def create_license(self, payload: dict):
        data = self._request(
            "POST",
            "licenses",
            {
                "select": "license_id,client_name,status,expires_at,notes,metadata,created_at,updated_at",
            },
            body=payload,
        )
        return data[0] if isinstance(data, list) and data else data

    def update_license(self, license_id: str, payload: dict):
        data = self._request(
            "PATCH",
            "licenses",
            {
                "license_id": f"eq.{license_id}",
                "select": "license_id,client_name,status,expires_at,notes,metadata,created_at,updated_at",
            },
            body=payload,
        )
        return data[0] if isinstance(data, list) and data else data

    def upsert_permission(self, payload: dict):
        data = self._request(
            "POST",
            "license_module_permissions",
            {
                "on_conflict": "license_id,module_id",
                "select": "license_id,module_id,is_allowed",
            },
            body=payload,
            extra_headers={
                "Prefer": "resolution=merge-duplicates,return=representation",
            },
        )
        return data[0] if isinstance(data, list) and data else data


    def delete_permissions_by_module(self, module_id: str):
        data = self._request(
            "DELETE",
            "license_module_permissions",
            {
                "module_id": f"eq.{module_id}",
                "select": "license_id,module_id,is_allowed",
            },
        )
        return data if isinstance(data, list) else []

    def delete_module(self, module_id: str):
        data = self._request(
            "DELETE",
            "modules",
            {
                "module_id": f"eq.{module_id}",
                "select": "module_id,module_label,area_id,area_label,is_active",
            },
        )
        if isinstance(data, list) and data:
            return data[0]
        return {"module_id": module_id}

    def can_access_module(self, license_id: str, module_id: str):
        result = self._request(
            "POST",
            "rpc/can_access_module",
            body={
                "p_license_id": license_id,
                "p_module_id": module_id,
            },
        )
        if isinstance(result, list) and result:
            return result[0]
        if isinstance(result, dict):
            return result
        return {"allowed": False, "reason": "invalid_rpc_response"}
