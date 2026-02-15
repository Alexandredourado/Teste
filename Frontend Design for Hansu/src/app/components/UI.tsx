import React from "react";
import { motion } from "motion/react";
import { ArrowUpRight, CheckCircle2, AlertCircle, Clock, ChevronRight, Download, Filter, Search, FileDown } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Module Card for Hub
export const ModuleCard = ({ title, description, icon: Icon, onClick, count }: any) => (
  <motion.div 
    whileHover={{ y: -4, boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)" }}
    onClick={onClick}
    className="bg-white dark:bg-slate-800 p-6 rounded-xl border border-hansu-border dark:border-white/10 cursor-pointer transition-all group"
  >
    <div className="flex justify-between items-start mb-4">
      <div className="w-12 h-12 bg-hansu-bg dark:bg-white/5 rounded-lg flex items-center justify-center text-hansu-primary group-hover:bg-hansu-primary group-hover:text-white transition-colors duration-300">
        <Icon className="w-6 h-6" />
      </div>
      {count && (
        <span className="bg-hansu-bg dark:bg-white/10 px-2 py-1 rounded text-[10px] font-bold text-slate-500 dark:text-slate-400">
          {count} MÓDULOS
        </span>
      )}
    </div>
    <h3 className="text-lg font-bold text-hansu-text dark:text-white mb-1 group-hover:text-hansu-primary transition-colors">{title}</h3>
    <p className="text-sm text-slate-500 dark:text-slate-400 mb-6 line-clamp-2">{description}</p>
    <div className="flex items-center text-hansu-primary font-bold text-sm">
      Acessar Área <ArrowUpRight className="w-4 h-4 ml-1" />
    </div>
  </motion.div>
);

// Status Badge
export const StatusBadge = ({ status, text }: { status: 'success' | 'error' | 'warning' | 'info' | 'active' | 'expired', text: string }) => {
  const styles = {
    success: "bg-green-50 text-hansu-success border-green-200",
    error: "bg-red-50 text-hansu-error border-red-200",
    warning: "bg-amber-50 text-amber-700 border-amber-200",
    info: "bg-blue-50 text-hansu-secondary border-blue-200",
    active: "bg-green-50 text-hansu-success border-green-200",
    expired: "bg-slate-50 text-slate-500 border-slate-200"
  };

  return (
    <span className={cn("px-2.5 py-0.5 rounded-full text-xs font-bold border", styles[status])}>
      {text}
    </span>
  );
};

// Data Table
export const DataTable = ({ columns, data, onExport, title }: any) => (
  <div className="bg-white dark:bg-slate-800 rounded-xl border border-hansu-border dark:border-white/10 overflow-hidden shadow-sm">
    <div className="p-6 border-b border-hansu-border dark:border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <h3 className="font-bold text-lg dark:text-white">{title}</h3>
      <div className="flex items-center gap-3">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            type="text" 
            placeholder="Filtrar..."
            className="pl-10 pr-4 py-2 text-sm border border-hansu-border dark:border-white/10 bg-hansu-bg dark:bg-white/5 rounded-lg w-full md:w-48"
          />
        </div>
        <button className="flex items-center gap-2 px-4 py-2 border border-hansu-border dark:border-white/10 rounded-lg text-sm font-bold text-hansu-neutral-dark dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/5 transition-all">
          <Filter className="w-4 h-4" /> Filtros
        </button>
        <button 
          onClick={onExport}
          className="flex items-center gap-2 px-4 py-2 bg-hansu-primary text-white rounded-lg text-sm font-bold hover:bg-hansu-primary-hover transition-all shadow-sm"
        >
          <FileDown className="w-4 h-4" /> Exportar
        </button>
      </div>
    </div>
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-slate-50 dark:bg-white/5 border-b border-hansu-border dark:border-white/10">
            {columns.map((col: any) => (
              <th key={col.key} className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                {col.label}
              </th>
            ))}
            <th className="px-6 py-4 text-right">Ações</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-hansu-border dark:divide-white/10">
          {data.map((row: any, i: number) => (
            <tr key={i} className="hover:bg-slate-50/50 dark:hover:bg-white/5 transition-colors">
              {columns.map((col: any) => (
                <td key={col.key} className="px-6 py-4 text-sm dark:text-slate-300">
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
              <td className="px-6 py-4 text-right">
                <button className="text-hansu-primary hover:text-hansu-primary-hover font-bold text-sm">Editar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    <div className="p-4 bg-slate-50 dark:bg-white/5 border-t border-hansu-border dark:border-white/10 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
      <div>Mostrando 1 a {data.length} de {data.length} registros</div>
      <div className="flex items-center gap-2">
        <button disabled className="px-3 py-1 border border-hansu-border dark:border-white/10 rounded bg-white dark:bg-slate-800 disabled:opacity-50">Anterior</button>
        <button className="px-3 py-1 border border-hansu-border dark:border-white/10 rounded bg-hansu-primary text-white">1</button>
        <button className="px-3 py-1 border border-hansu-border dark:border-white/10 rounded bg-white dark:bg-slate-800">Próximo</button>
      </div>
    </div>
  </div>
);

// Progress Display
export const ProcessingProgress = ({ progress, fileName }: { progress: number, fileName: string }) => (
  <div className="bg-white dark:bg-slate-800 p-8 rounded-xl border border-hansu-border dark:border-white/10 shadow-lg max-w-2xl mx-auto">
    <div className="flex items-center justify-between mb-2">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-blue-50 dark:bg-blue-900/20 flex items-center justify-center rounded-lg">
          <Clock className="w-5 h-5 text-hansu-primary" />
        </div>
        <div>
          <div className="text-sm font-bold dark:text-white">Processando Arquivo</div>
          <div className="text-xs text-slate-500 dark:text-slate-400">{fileName}</div>
        </div>
      </div>
      <div className="text-lg font-bold text-hansu-primary">{progress}%</div>
    </div>
    <div className="w-full bg-slate-100 dark:bg-white/10 h-3 rounded-full overflow-hidden mt-4">
      <motion.div 
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        className="bg-hansu-primary h-full rounded-full"
      />
    </div>
    <div className="mt-6 flex justify-between items-center">
      <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
        <div className="w-2 h-2 bg-hansu-primary rounded-full animate-pulse" />
        Extraindo dados do PDF...
      </div>
      <button className="text-sm font-bold text-hansu-error">Cancelar</button>
    </div>
  </div>
);
