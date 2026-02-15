export interface ApiModule {
  id: string;
  title: string;
  description: string;
  action: string;
  type: 'upload' | 'table' | 'edit';
}

export interface ApiArea {
  id: string;
  label: string;
  modules: {
    id: string;
    label: string;
    description: string;
  }[];
}

export interface ApiLicense {
  id: string;
  cliente: string;
  modulo: string;
  status: string;
  expira: string;
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Erro ${response.status} ao chamar ${path}`);
  }

  return response.json() as Promise<T>;
}

function resolveType(moduleId: string): ApiModule['type'] {
  return moduleId.includes('editor') ? 'edit' : 'upload';
}

function resolveAction(moduleId: string): string {
  return moduleId.includes('editor') ? 'Abrir Editor' : 'Iniciar Extração';
}

export async function fetchAreasModules(): Promise<Record<string, ApiModule[]>> {
  const areas = await getJson<ApiArea[]>('/modules/areas');

  return areas.reduce<Record<string, ApiModule[]>>((acc, area) => {
    acc[area.id] = area.modules.map((module) => ({
      id: module.id,
      title: module.label,
      description: module.description,
      type: resolveType(module.id),
      action: resolveAction(module.id),
    }));
    return acc;
  }, {});
}

export async function fetchLicenses(): Promise<ApiLicense[]> {
  return getJson<ApiLicense[]>('/licenses');
}
