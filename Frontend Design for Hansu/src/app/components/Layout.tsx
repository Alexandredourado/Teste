import React from "react";
import { motion } from "motion/react";
import { 
  LayoutDashboard, 
  FileText, 
  Briefcase, 
  Settings, 
  ShieldCheck, 
  ChevronRight,
  LogOut,
  Bell,
  Search,
  User,
  Sun,
  Moon
} from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export type Page = 'hub' | 'ecac' | 'efd-contrib' | 'efd-icms' | 'admin' | 'activation' | 'settings';

interface SidebarProps {
  currentPage: Page;
  setCurrentPage: (page: Page) => void;
}

export const Sidebar = ({ currentPage, setCurrentPage }: SidebarProps) => {
  const menuItems = [
    { id: 'hub', label: 'Hub (Home)', icon: LayoutDashboard },
    { id: 'ecac', label: 'Ecac', icon: FileText },
    { id: 'efd-contrib', label: 'EFD Contribuições', icon: Briefcase },
    { id: 'efd-icms', label: 'EFD ICMS', icon: Briefcase },
    { id: 'admin', label: 'Administrador', icon: ShieldCheck },
  ];

  return (
    <div className="w-[280px] h-screen fixed left-0 top-0 bg-linear-to-b from-hansu-sidebar-start to-hansu-sidebar-end text-white flex flex-col z-50">
      <div className="p-8 flex items-center gap-3">
        <div className="w-10 h-10 bg-hansu-primary rounded-lg flex items-center justify-center font-bold text-xl shadow-lg">
          H
        </div>
        <span className="text-2xl font-bold tracking-tight">HANSU</span>
      </div>

      <nav className="flex-1 px-4 mt-4 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentPage(item.id as Page)}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group",
                isActive 
                  ? "bg-hansu-primary text-white shadow-md" 
                  : "text-slate-400 hover:bg-white/5 hover:text-white"
              )}
            >
              <Icon className={cn("w-5 h-5", isActive ? "text-white" : "group-hover:text-hansu-secondary")} />
              <span className="font-medium flex-1 text-left">{item.label}</span>
              {isActive && (
                <motion.div layoutId="active-indicator">
                  <ChevronRight className="w-4 h-4" />
                </motion.div>
              )}
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/10 space-y-1">
        <button 
          onClick={() => setCurrentPage('settings')}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-white/5 hover:text-white transition-all"
        >
          <Settings className="w-5 h-5" />
          <span className="font-medium">Configurações</span>
        </button>
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-hansu-error hover:bg-red-500/10 transition-all">
          <LogOut className="w-5 h-5" />
          <span className="font-medium">Sair</span>
        </button>
      </div>

      <div className="p-6 bg-white/5 mx-4 mb-8 rounded-xl border border-white/10">
        <div className="text-xs text-slate-400 mb-1">Licença Ativa</div>
        <div className="text-sm font-semibold truncate">Hansu Enterprise Pro</div>
        <div className="mt-2 w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
          <div className="bg-hansu-success h-full w-[75%]" />
        </div>
        <div className="text-[10px] text-slate-400 mt-1 text-right">75 dias restantes</div>
      </div>
    </div>
  );
};

interface HeaderProps {
  currentPage: Page;
  isDarkMode: boolean;
  setIsDarkMode: (val: boolean) => void;
}

export const Header = ({ currentPage, isDarkMode, setIsDarkMode }: HeaderProps) => {
  const getPageTitle = () => {
    switch (currentPage) {
      case 'hub': return 'Hub de Operações';
      case 'ecac': return 'Ecac - Central de Extração';
      case 'efd-contrib': return 'EFD Contribuições';
      case 'efd-icms': return 'EFD ICMS';
      case 'admin': return 'Painel Administrativo';
      case 'activation': return 'Ativação de Licença';
      case 'settings': return 'Configurações de Perfil';
      default: return 'Hansu';
    }
  };

  return (
    <header className="h-20 bg-white dark:bg-hansu-sidebar-start border-b border-hansu-border dark:border-white/10 flex items-center justify-between px-8 sticky top-0 z-40 backdrop-blur-md bg-white/80 dark:bg-slate-900/80">
      <div className="flex flex-col">
        <div className="text-xs text-slate-500 font-medium flex items-center gap-2">
          Sistema Hansu <ChevronRight className="w-3 h-3" /> {getPageTitle()}
        </div>
        <h1 className="text-xl font-bold text-hansu-text dark:text-white">{getPageTitle()}</h1>
      </div>

      <div className="flex items-center gap-6">
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            type="text" 
            placeholder="Buscar módulos ou arquivos..."
            className="pl-10 pr-4 py-2 bg-hansu-bg dark:bg-white/5 border border-hansu-border dark:border-white/10 rounded-lg text-sm w-64 focus:outline-none focus:ring-2 focus:ring-hansu-primary/20 transition-all"
          />
        </div>

        <div className="flex items-center gap-2">
          <button 
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="p-2 text-slate-500 hover:bg-slate-100 dark:hover:bg-white/5 rounded-lg transition-all"
          >
            {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
          
          <button className="p-2 text-slate-500 hover:bg-slate-100 dark:hover:bg-white/5 rounded-lg transition-all relative">
            <Bell className="w-5 h-5" />
            <span className="absolute top-2 right-2 w-2 h-2 bg-hansu-error rounded-full border-2 border-white dark:border-slate-900" />
          </button>
        </div>

        <div className="flex items-center gap-3 pl-6 border-l border-hansu-border dark:border-white/10">
          <div className="text-right hidden sm:block">
            <div className="text-sm font-bold text-hansu-text dark:text-white leading-tight">Admin User</div>
            <div className="text-[10px] text-slate-500 font-medium">Administrador Geral</div>
          </div>
          <div className="w-10 h-10 bg-hansu-secondary rounded-full flex items-center justify-center text-white font-bold shadow-md">
            AD
          </div>
        </div>
      </div>
    </header>
  );
};
