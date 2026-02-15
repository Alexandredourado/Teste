from .module_registry import (
    MODULES,
    ModuleEntry,
    get_module,
    list_areas_with_modules,
    list_module_catalog,
    list_module_entries,
)
from .supabase_client import (
    SupabaseConfigError,
    SupabaseLicenseService,
    SupabaseRequestError,
)

__all__ = [
    "MODULES",
    "ModuleEntry",
    "get_module",
    "list_areas_with_modules",
    "list_module_entries",
    "list_module_catalog",
    "SupabaseConfigError",
    "SupabaseLicenseService",
    "SupabaseRequestError",
]
