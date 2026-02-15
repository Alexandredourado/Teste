import React from "react";
import { motion } from "motion/react";
import { 
  FileText, 
  Briefcase, 
  ShieldCheck, 
  TrendingUp, 
  AlertCircle, 
  CheckCircle2, 
  Calendar,
  Zap,
  Clock,
  ChevronRight
} from "lucide-react";
import { ModuleCard, StatusBadge } from "../components/UI";
import { Page } from "../components/Layout";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

const data = [
  { name: '01/02', extractions: 45 },
  { name: '03/02', extractions: 52 },
  { name: '05/02', extractions: 38 },
  { name: '07/02', extractions: 65 },
  { name: '09/02', extractions: 48 },
  { name: '11/02', extractions: 72 },
  { name: '13/02', extractions: 58 },
  { name: '15/02', extractions: 84 },
];

export const Hub = ({ setPage }: { setPage: (p: Page) => void }) => {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Welcome Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-hansu-text dark:text-white">Bom dia, Administrador</h2>
          <p className="text-slate-500 dark:text-slate-400">Aqui está o resumo da operação Hansu hoje.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="bg-white dark:bg-slate-800 px-4 py-2 rounded-lg border border-hansu-border dark:border-white/10 shadow-sm flex items-center gap-2">
            <Calendar className="w-4 h-4 text-hansu-primary" />
            <span className="text-sm font-bold dark:text-white">15 de Fevereiro, 2026</span>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Arquivos Processados', value: '1,284', trend: '+12%', icon: FileText, color: 'text-hansu-primary' },
          { label: 'Extrações Bem-sucedidas', value: '98.2%', trend: '+0.5%', icon: CheckCircle2, color: 'text-hansu-success' },
          { label: 'Pendências Técnicas', value: '14', trend: '-2', icon: AlertCircle, color: 'text-hansu-error' },
          { label: 'Licenças Ativas', value: '42', trend: 'Estável', icon: ShieldCheck, color: 'text-hansu-secondary' },
        ].map((stat, i) => (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            key={stat.label} 
            className="bg-white dark:bg-slate-800 p-6 rounded-xl border border-hansu-border dark:border-white/10 shadow-sm"
          >
            <div className="flex items-center justify-between mb-2">
              <div className={cn("p-2 rounded-lg bg-slate-50 dark:bg-white/5", stat.color)}>
                <stat.icon className="w-5 h-5" />
              </div>
              <span className={cn(
                "text-xs font-bold px-2 py-0.5 rounded-full",
                stat.trend.startsWith('+') ? "bg-green-50 text-hansu-success" : 
                stat.trend.startsWith('-') ? "bg-red-50 text-hansu-error" : "bg-slate-50 text-slate-500"
              )}>
                {stat.trend}
              </span>
            </div>
            <div className="text-2xl font-bold text-hansu-text dark:text-white">{stat.value}</div>
            <div className="text-sm text-slate-500 dark:text-slate-400">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Main Grid: Modules & Analytics */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        <div className="xl:col-span-2 space-y-8">
          {/* Areas Section */}
          <div>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-bold dark:text-white flex items-center gap-2">
                <Zap className="w-5 h-5 text-hansu-secondary" /> Áreas do Hub
              </h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ModuleCard 
                title="Ecac" 
                description="Extração de Darf, DCTFWeb e Declarações Simples Nacional (PGDAS) de forma automatizada."
                icon={FileText}
                count={3}
                onClick={() => setPage('ecac')}
              />
              <ModuleCard 
                title="EFD Contribuições" 
                description="Módulo dedicado a Extrator M200/M600 e Editor de CNPJ nos registros SPED."
                icon={Briefcase}
                count={2}
                onClick={() => setPage('efd-contrib')}
              />
              <ModuleCard 
                title="EFD ICMS" 
                description="Extração de registros E110/E115, Inventário H005 e editor assistido de CNPJ/IE."
                icon={Briefcase}
                count={3}
                onClick={() => setPage('efd-icms')}
              />
              <ModuleCard 
                title="Administrador" 
                description="Gestão de licenças digitais, controle de permissões por módulo e logs do sistema."
                icon={ShieldCheck}
                count={2}
                onClick={() => setPage('admin')}
              />
            </div>
          </div>

          {/* Activity Chart */}
          <div className="bg-white dark:bg-slate-800 p-8 rounded-xl border border-hansu-border dark:border-white/10 shadow-sm">
            <div className="flex items-center justify-between mb-8">
              <h3 className="font-bold text-lg dark:text-white">Volume de Extrações (Últimos 15 dias)</h3>
              <div className="flex items-center gap-2">
                <span className="flex items-center gap-1 text-xs text-hansu-success font-bold">
                  <TrendingUp className="w-4 h-4" /> +24% em relação ao mês anterior
                </span>
              </div>
            </div>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                  <defs>
                    <linearGradient id="colorEx" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#1570EF" stopOpacity={0.1}/>
                      <stop offset="95%" stopColor="#1570EF" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
                  <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#64748b'}} />
                  <Tooltip 
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                  />
                  <Area type="monotone" dataKey="extractions" stroke="#1570EF" strokeWidth={3} fillOpacity={1} fill="url(#colorEx)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Sidebar: Recent Activity & Notifications */}
        <div className="space-y-8">
          <div className="bg-white dark:bg-slate-800 rounded-xl border border-hansu-border dark:border-white/10 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-hansu-border dark:border-white/10 flex items-center justify-between">
              <h3 className="font-bold dark:text-white">Histórico Recente</h3>
              <button className="text-hansu-primary text-xs font-bold hover:underline">Ver todos</button>
            </div>
            <div className="p-4 space-y-4">
              {[
                { type: 'upload', title: 'DCTFWeb Extraída', time: '12 min atrás', status: 'success' },
                { type: 'edit', title: 'CNPJ Alterado (SPED)', time: '45 min atrás', status: 'info' },
                { type: 'license', title: 'Licença Gerada #8842', time: '2h atrás', status: 'active' },
                { type: 'error', title: 'Erro de Leitura PGDAS', time: '5h atrás', status: 'error' },
              ].map((item, i) => (
                <div key={i} className="flex gap-3 p-2 hover:bg-slate-50 dark:hover:bg-white/5 rounded-lg transition-all cursor-pointer group">
                  <div className={cn(
                    "w-10 h-10 rounded-lg flex items-center justify-center shrink-0",
                    item.status === 'success' ? "bg-green-50 text-hansu-success" :
                    item.status === 'error' ? "bg-red-50 text-hansu-error" : "bg-blue-50 text-hansu-secondary"
                  )}>
                    <Clock className="w-5 h-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-bold text-hansu-text dark:text-white truncate group-hover:text-hansu-primary transition-colors">{item.title}</div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">{item.time}</div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-300 self-center" />
                </div>
              ))}
            </div>
          </div>

          <div className="bg-linear-to-br from-hansu-primary to-hansu-primary-hover p-8 rounded-xl text-white shadow-lg relative overflow-hidden group">
            <div className="relative z-10">
              <h4 className="text-lg font-bold mb-2">Precisa de Ajuda?</h4>
              <p className="text-white/80 text-sm mb-6">Acesse nossa base de conhecimento ou fale com o suporte técnico.</p>
              <button className="bg-white text-hansu-primary px-6 py-2 rounded-lg font-bold text-sm hover:bg-slate-100 transition-all shadow-md flex items-center gap-2">
                Suporte Hansu <ChevronRight className="w-4 h-4" />
              </button>
            </div>
            <ShieldCheck className="absolute -bottom-6 -right-6 w-32 h-32 text-white/10 group-hover:scale-110 transition-transform duration-500" />
          </div>
        </div>
      </div>
    </div>
  );
};

function cn(...inputs: any[]) {
  return inputs.filter(Boolean).join(' ');
}
