import React, { useState } from "react";
import { Toaster } from "sonner";
import { Sidebar, Header, Page } from "./components/Layout";
import { Hub } from "./pages/Hub";
import { ModulePage, AdminPage } from "./pages/Modules";
import { Activation } from "./pages/Activation";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('activation');
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isActivated, setIsActivated] = useState(false);

  // Define module structures for different areas
  const ecacModules = [
    { id: 'darf', title: 'Extrair Darf', description: 'Upload de PDF para processamento e exportação para Excel.', action: 'Iniciar Extração', type: 'upload' as const },
    { id: 'dctf', title: 'Extrair DCTFWeb', description: 'Extração de Débitos, Créditos e Compensações via leitura de PDF.', action: 'Iniciar Extração', type: 'upload' as const },
    { id: 'pgdas', title: 'PGDAS Simples Nacional', description: 'Leitura por atividade/segregação e débitos apurados.', action: 'Iniciar Extração', type: 'upload' as const },
  ];

  const efdContribModules = [
    { id: 'm200', title: 'Extrator M200/M600', description: 'Seleção de arquivo SPED, visualização de registros e validações.', action: 'Selecionar SPED', type: 'upload' as const },
    { id: 'editor-cnpj', title: 'Editor CNPJ', description: 'Busca de arquivo e edição assistida do registro |0000|.', action: 'Abrir Editor', type: 'edit' as const },
  ];

  const efdIcmsModules = [
    { id: 'e110', title: 'Extrator E110/E115', description: 'Leitura dos registros SPED e exportação tabular.', action: 'Selecionar SPED', type: 'upload' as const },
    { id: 'editor-cnpj-ie', title: 'Editor CNPJ/IE', description: 'Atualização de CNPJ e IE no registro |0000| com validação.', action: 'Abrir Editor', type: 'edit' as const },
    { id: 'h005', title: 'Extrator Inventário H005', description: 'Extração de inventário H005 e consolidação Excel.', action: 'Selecionar SPED', type: 'upload' as const },
  ];

  const renderContent = () => {
    switch (currentPage) {
      case 'hub':
        return <Hub setPage={setCurrentPage} />;
      case 'ecac':
        return <ModulePage area="Ecac" modules={ecacModules} />;
      case 'efd-contrib':
        return <ModulePage area="EFD Contribuições" modules={efdContribModules} />;
      case 'efd-icms':
        return <ModulePage area="EFD ICMS" modules={efdIcmsModules} />;
      case 'admin':
        return <AdminPage />;
      case 'settings':
        return (
          <div className="bg-white dark:bg-slate-800 p-8 rounded-xl border border-hansu-border dark:border-white/10 max-w-2xl">
            <h2 className="text-xl font-bold dark:text-white mb-6">Configurações do Perfil</h2>
            <div className="space-y-4">
              <div className="flex items-center gap-4 p-4 border border-hansu-border dark:border-white/10 rounded-lg">
                <div className="w-16 h-16 bg-hansu-primary rounded-full flex items-center justify-center text-white text-xl font-bold">AD</div>
                <div>
                  <div className="font-bold dark:text-white">Admin Hansu</div>
                  <div className="text-sm text-slate-500">admin@hansu.com.br</div>
                </div>
                <button className="ml-auto text-sm font-bold text-hansu-primary">Alterar Foto</button>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-500 mb-1">Nome Completo</label>
                  <input type="text" defaultValue="Administrador Sistema" className="w-full p-2 border border-hansu-border dark:border-white/10 dark:bg-white/5 dark:text-white rounded" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-500 mb-1">E-mail</label>
                  <input type="email" defaultValue="admin@hansu.com.br" className="w-full p-2 border border-hansu-border dark:border-white/10 dark:bg-white/5 dark:text-white rounded" />
                </div>
              </div>
              <button className="w-full py-2 bg-hansu-primary text-white font-bold rounded-lg mt-4">Salvar Alterações</button>
            </div>
          </div>
        );
      default:
        return <Hub setPage={setCurrentPage} />;
    }
  };

  const handleActivation = () => {
    setIsActivated(true);
    setCurrentPage('hub');
  };

  if (!isActivated && currentPage === 'activation') {
    return (
      <div className={cn(isDarkMode ? "dark" : "")}>
        <Activation onActivate={handleActivation} />
        <Toaster position="top-right" expand={true} richColors />
      </div>
    );
  }

  return (
    <div className={cn(isDarkMode ? "dark bg-[#0B1730]" : "bg-hansu-bg", "min-h-screen transition-colors duration-300")}>
      <Toaster position="top-right" expand={true} richColors />
      
      <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      
      <main className="pl-[280px] flex flex-col min-h-screen">
        <Header 
          currentPage={currentPage} 
          isDarkMode={isDarkMode} 
          setIsDarkMode={setIsDarkMode} 
        />
        
        <div className="flex-1 p-8 container mx-auto">
          {renderContent()}
        </div>
        
        <footer className="p-8 text-center text-xs text-slate-500 dark:text-slate-400 border-t border-hansu-border dark:border-white/10">
          Hansu v2.4.0 — Inteligência Fiscal Automatizada | © 2026
        </footer>
      </main>
    </div>
  );
}
