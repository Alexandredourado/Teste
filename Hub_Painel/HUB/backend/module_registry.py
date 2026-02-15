from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModuleEntry:
    module_id: str
    area_id: str
    area_label: str
    label: str
    description: str
    script_path: Path


BASE_DIR = Path(__file__).resolve().parents[2]


MODULES: tuple[ModuleEntry, ...] = (
    ModuleEntry(
        module_id="extrair_darf",
        area_id="ecac",
        area_label="Ecac",
        label="Extrair Darf",
        description="Abre o módulo de extração de DARF em PDF para Excel.",
        script_path=BASE_DIR / "Extrator-Darf" / "Extrair_Darf.py",
    ),
    ModuleEntry(
        module_id="extrair_dctfweb",
        area_id="ecac",
        area_label="Ecac",
        label="Extrair DCTFWeb",
        description="Abre o módulo de extração de declaração DCTFWeb (Débito/Crédito e Compensações).",
        script_path=BASE_DIR / "Extrator-DCTFWeb" / "Extrair_DCTFWeb.py",
    ),
    ModuleEntry(
        module_id="declaracao_pgdas",
        area_id="ecac",
        area_label="Ecac",
        label="Declaração Simples Nacional",
        description="Abre o módulo de análise da Declaração Simples Nacional (PDF para segregação por atividade e débitos apurados).",
        script_path=BASE_DIR / "DECLARACAO_PGDAS" / "open_frontend.py",
    ),
    ModuleEntry(
        module_id="efd_contrib_extrator",
        area_id="efd_contribuicoes",
        area_label="EFD Contribuições",
        label="EFD Contribuições • Extrator M200/M600",
        description="Abre o módulo de extração dos registros M200 e M600 dos arquivos SPED.",
        script_path=BASE_DIR / "EFD_CONTRIBUICOES" / "open_frontend.py",
    ),
    ModuleEntry(
        module_id="efd_contrib_editor",
        area_id="efd_contribuicoes",
        area_label="EFD Contribuições",
        label="EFD Contribuições • Editor CNPJ",
        description="Abre o módulo de edição do CNPJ no registro |0000| dos arquivos de contribuições.",
        script_path=BASE_DIR / "EFD_CONTRIBUICOES" / "open_frontend.py",
    ),
    ModuleEntry(
        module_id="efd_icms_extrator",
        area_id="efd_icms",
        area_label="EFD ICMS",
        label="EFD ICMS • Extrator E110/E115",
        description="Abre o módulo de extração dos registros E110 e E115.",
        script_path=BASE_DIR / "EFD_ICMS" / "open_frontend.py",
    ),
    ModuleEntry(
        module_id="efd_icms_editor",
        area_id="efd_icms",
        area_label="EFD ICMS",
        label="EFD ICMS • Editor CNPJ/IE",
        description="Abre o módulo de atualização de CNPJ e IE no registro |0000|.",
        script_path=BASE_DIR / "EFD_ICMS" / "open_frontend.py",
    ),
    ModuleEntry(
        module_id="efd_icms_h005",
        area_id="efd_icms",
        area_label="EFD ICMS",
        label="EFD ICMS • Extrator H005",
        description="Abre o módulo de extração de inventário H005 com exportação de Excel consolidado.",
        script_path=BASE_DIR / "EFD_ICMS" / "open_frontend.py",
    ),
    ModuleEntry(
        module_id="gerar_licenca",
        area_id="administrador",
        area_label="Administrador",
        label="Gerar Licença",
        description="Abre o gerador de licença digital (v1 + license_id).",
        script_path=BASE_DIR / "LICENÇAS" / "gerador_licenca.py",
    ),
    ModuleEntry(
        module_id="painel_administrativo_supabase",
        area_id="administrador",
        area_label="Administrador",
        label="Painel Administrativo",
        description="Abre o painel administrativo do servidor para status e permissões de licenças.",
        script_path=BASE_DIR / "HUB" / "painel_administrativo_supabase.py",
    ),
)


def list_module_entries() -> list[ModuleEntry]:
    return list(MODULES)


def list_module_catalog() -> list[dict]:
    return [
        {
            "module_id": module.module_id,
            "module_label": module.label,
            "area_id": module.area_id,
            "area_label": module.area_label,
            "is_active": True,
        }
        for module in MODULES
    ]


def list_areas_with_modules() -> list[dict]:
    grouped: dict[str, dict] = {}

    for module in MODULES:
        area = grouped.setdefault(
            module.area_id,
            {
                "id": module.area_id,
                "label": module.area_label,
                "modules": [],
            },
        )
        area["modules"].append(
            {
                "id": module.module_id,
                "label": module.label,
                "description": module.description,
            }
        )

    return list(grouped.values())


def get_module(module_id: str) -> ModuleEntry | None:
    for module in MODULES:
        if module.module_id == module_id:
            return module
    return None
