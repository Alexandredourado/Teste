import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Upload, FileText, Download, CheckCircle2, AlertCircle, FileSpreadsheet, Search, Plus, Filter, Lock } from "lucide-react";
import { DataTable, ProcessingProgress, StatusBadge } from "../components/UI";
import { toast } from "sonner";

interface ModulePageProps {
  area: string;
  modules: {
    id: string;
    title: string;
    description: string;
    action: string;
    type: 'upload' | 'table' | 'edit';
  }[];
}

export const ModulePage = ({ area, modules }: ModulePageProps) => {
  const [activeModule, setActiveModule] = useState<string | null>(null);
  const [view, setView] = useState<'selection' | 'execution' | 'result'>('selection');
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);

  const [editStep, setEditStep] = useState<'search' | 'edit' | 'review'>('search');

  const handleStartModule = (id: string) => {
    setActiveModule(id);
    const mod = modules.find(m => m.id === id);
    if (mod?.type === 'edit') {
      setView('execution');
      setEditStep('search');
    } else {
      setView('execution');
    }
  };

  const handleEditConfirm = () => {
    toast.success("Registro atualizado com sucesso!");
    setView('result');
  };

  if (view === 'execution' && modules.find(m => m.id === activeModule)?.type === 'edit') {
    return (
      <div className="max-w-3xl mx-auto py-12">
        <button onClick={() => setView('selection')} className="text-sm font-bold text-hansu-primary mb-8 flex items-center gap-2">
          ← Voltar para {area}
        </button>
        
        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-hansu-border dark:border-white/10 p-10 shadow-xl">
          <div className="flex items-center gap-4 mb-8">
            <div className="w-12 h-12 bg-hansu-primary/10 rounded-xl flex items-center justify-center text-hansu-primary">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-2xl font-bold dark:text-white">Editor de Registro |0000|</h2>
              <p className="text-sm text-slate-500">Ajuste técnico de CNPJ/IE nos arquivos SPED.</p>
            </div>
          </div>

          <div className="space-y-6">
            <div className="p-4 bg-hansu-bg dark:bg-white/5 rounded-lg border border-hansu-border dark:border-white/10">
              <div className="text-xs font-bold text-slate-500 uppercase mb-3">Valor Atual no Arquivo</div>
              <div className="font-mono text-hansu-neutral-dark dark:text-slate-300">|0000|006|0|01012026|31012026|EMPRESA EXEMPLO LTDA|12345678000190|...|</div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-bold text-slate-500 mb-1">Novo CNPJ</label>
                <input type="text" placeholder="00.000.000/0000-00" className="w-full p-3 border border-hansu-border dark:bg-white/5 dark:text-white rounded-xl focus:ring-2 focus:ring-hansu-primary/20 outline-none" />
              </div>
              <div>
                <label className="block text-sm font-bold text-slate-500 mb-1">Nova Inscrição Estadual</label>
                <input type="text" placeholder="ISENTO" className="w-full p-3 border border-hansu-border dark:bg-white/5 dark:text-white rounded-xl focus:ring-2 focus:ring-hansu-primary/20 outline-none" />
              </div>
            </div>

            <div className="flex gap-4 pt-4">
              <button 
                onClick={handleEditConfirm}
                className="flex-1 py-3 bg-hansu-primary text-white font-bold rounded-xl shadow-lg shadow-hansu-primary/20 hover:bg-hansu-primary-hover transition-all"
              >
                Confirmar Alteração
              </button>
              <button onClick={() => setView('selection')} className="px-8 py-3 bg-white dark:bg-slate-700 border border-hansu-border dark:border-white/10 rounded-xl font-bold dark:text-white">
                Cancelar
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Mock data for results
  const mockTableData = [
    { id: '1', data: '15/02/2026', valor: 'R$ 1.250,00', status: 'Processado', usuario: 'Admin' },
    { id: '2', data: '14/02/2026', valor: 'R$ 3.420,50', status: 'Processado', usuario: 'Admin' },
    { id: '3', data: '12/02/2026', valor: 'R$ 890,00', status: 'Erro', usuario: 'User' },
    { id: '4', data: '10/02/2026', valor: 'R$ 2.100,00', status: 'Processado', usuario: 'Admin' },
  ];

  const columns = [
    { key: 'data', label: 'Data Processamento' },
    { key: 'valor', label: 'Valor Apurado' },
    { 
      key: 'status', 
      label: 'Status',
      render: (val: string) => <StatusBadge status={val === 'Processado' ? 'success' : 'error'} text={val} />
    },
    { key: 'usuario', label: 'Usuário' },
  ];

  if (view === 'selection') {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold dark:text-white">Módulos Disponíveis em {area}</h2>
          <div className="flex gap-2">
            <button className="px-4 py-2 border border-hansu-border dark:border-white/10 rounded-lg text-sm font-bold bg-white dark:bg-slate-800 dark:text-white hover:bg-slate-50 transition-all">
              Ver Histórico Geral
            </button>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((mod) => (
            <motion.div 
              key={mod.id}
              whileHover={{ y: -4 }}
              className="bg-white dark:bg-slate-800 p-6 rounded-xl border border-hansu-border dark:border-white/10 shadow-sm flex flex-col h-full"
            >
              <div className="w-10 h-10 bg-hansu-bg dark:bg-white/5 rounded-lg flex items-center justify-center text-hansu-primary mb-4">
                <FileText className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-lg dark:text-white mb-2">{mod.title}</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mb-6 flex-1">{mod.description}</p>
              <button 
                onClick={() => handleStartModule(mod.id)}
                className="w-full py-2.5 bg-hansu-primary text-white font-bold rounded-lg text-sm hover:bg-hansu-primary-hover transition-all"
              >
                {mod.action}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    );
  }

  if (view === 'execution') {
    return (
      <div className="max-w-4xl mx-auto py-12">
        <button onClick={() => setView('selection')} className="text-sm font-bold text-hansu-primary mb-8 flex items-center gap-2">
          ← Voltar para {area}
        </button>
        
        {isProcessing ? (
          <ProcessingProgress progress={progress} fileName="extração_fiscal_hansu_2026.pdf" />
        ) : (
          <div className="bg-white dark:bg-slate-800 rounded-2xl border-2 border-dashed border-hansu-border dark:border-white/10 p-16 text-center shadow-lg">
            <div className="w-20 h-20 bg-hansu-bg dark:bg-white/5 rounded-full flex items-center justify-center mx-auto mb-6">
              <Upload className="w-10 h-10 text-hansu-primary" />
            </div>
            <h2 className="text-2xl font-bold dark:text-white mb-2">Upload de Arquivo</h2>
            <p className="text-slate-500 dark:text-slate-400 mb-8 max-w-sm mx-auto">
              Arraste o arquivo PDF ou SPED para processamento ou clique para selecionar do seu computador.
            </p>
            <div className="flex flex-col gap-3 max-w-xs mx-auto">
              <button 
                onClick={simulateProcessing}
                className="w-full py-4 bg-hansu-primary text-white font-bold rounded-xl shadow-lg shadow-hansu-primary/20 hover:scale-[1.02] transition-all"
              >
                Selecionar Arquivo
              </button>
              <p className="text-[10px] text-slate-400 uppercase tracking-widest font-bold">PDF, TXT ou Excel (Máx. 50MB)</p>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => setView('execution')} className="p-2 hover:bg-white dark:hover:bg-slate-800 rounded-lg border border-hansu-border dark:border-white/10">
            ←
          </button>
          <div>
            <h2 className="text-xl font-bold dark:text-white">Resultado da Extração</h2>
            <p className="text-sm text-slate-500">Módulo: {modules.find(m => m.id === activeModule)?.title}</p>
          </div>
        </div>
        <div className="flex gap-3">
          <button className="flex items-center gap-2 px-6 py-2 bg-hansu-success text-white font-bold rounded-lg text-sm shadow-md">
            <FileSpreadsheet className="w-4 h-4" /> Exportar Excel
          </button>
          <button onClick={() => setView('selection')} className="px-6 py-2 bg-white dark:bg-slate-800 border border-hansu-border dark:border-white/10 rounded-lg text-sm font-bold dark:text-white">
            Finalizar Fluxo
          </button>
        </div>
      </div>

      <DataTable 
        title="Dados Extraídos" 
        columns={columns} 
        data={mockTableData} 
        onExport={() => toast.success("Exportando arquivo...")} 
      />
    </div>
  );
};

// Admin Page Component
export const AdminPage = () => {
  const [tab, setTab] = useState<'licencas' | 'permissoes'>('licencas');

  const licenses = [
    { id: 'LIC-001', cliente: 'Contabilidade Silva', modulo: 'Hansu Hub', status: 'Ativa', expira: '15/05/2026' },
    { id: 'LIC-002', cliente: 'Empresa XPTO', modulo: 'Full Access', status: 'Ativa', expira: '20/12/2026' },
    { id: 'LIC-003', cliente: 'Escritório Digital', modulo: 'Ecac + EFD', status: 'Expirando', expira: '28/02/2026' },
    { id: 'LIC-004', cliente: 'Logística S.A', modulo: 'Ecac', status: 'Suspensa', expira: 'Expired' },
  ];

  const columns = [
    { key: 'id', label: 'ID Licença' },
    { key: 'cliente', label: 'Cliente/Operação' },
    { key: 'modulo', label: 'Módulos Habilitados' },
    { key: 'expira', label: 'Data Expiração' },
    { 
      key: 'status', 
      label: 'Status',
      render: (val: string) => {
        const s = val === 'Ativa' ? 'success' : val === 'Expirando' ? 'warning' : 'error';
        return <StatusBadge status={s} text={val} />
      }
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex bg-white dark:bg-slate-800 p-1 rounded-xl border border-hansu-border dark:border-white/10 w-fit">
          <button 
            onClick={() => setTab('licencas')}
            className={cn(
              "px-6 py-2 rounded-lg text-sm font-bold transition-all",
              tab === 'licencas' ? "bg-hansu-primary text-white shadow-md" : "text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-white/5"
            )}
          >
            Gestão de Licenças
          </button>
          <button 
            onClick={() => setTab('permissoes')}
            className={cn(
              "px-6 py-2 rounded-lg text-sm font-bold transition-all",
              tab === 'permissoes' ? "bg-hansu-primary text-white shadow-md" : "text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-white/5"
            )}
          >
            Matriz de Permissões
          </button>
        </div>
        <button className="flex items-center gap-2 px-6 py-2.5 bg-hansu-primary text-white font-bold rounded-lg text-sm shadow-lg shadow-hansu-primary/20">
          <Plus className="w-4 h-4" /> Gerar Nova Licença
        </button>
      </div>

      {tab === 'licencas' ? (
        <DataTable 
          title="Licenças Ativas no Sistema" 
          columns={columns} 
          data={licenses} 
          onExport={() => toast.success("Exportando relatório de licenças...")} 
        />
      ) : (
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-hansu-border dark:border-white/10 p-12 text-center">
          <Lock className="w-12 h-12 text-slate-300 mx-auto mb-4" />
          <h3 className="font-bold text-lg dark:text-white">Matriz de Permissões do Sistema</h3>
          <p className="text-slate-500 max-w-md mx-auto mb-8">Defina quais módulos cada nível de usuário ou chave de licença pode acessar e operar.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {['Visualizador', 'Operador', 'Administrador'].map(level => (
              <div key={level} className="p-6 border border-hansu-border dark:border-white/10 rounded-xl hover:border-hansu-primary transition-colors cursor-pointer text-left">
                <div className="font-bold mb-4 flex items-center justify-between">
                  {level}
                  <CheckCircle2 className="w-4 h-4 text-hansu-success" />
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span>Acesso Ecac</span>
                    <span className="font-bold text-hansu-success">SIM</span>
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span>Extração EFD</span>
                    <span className="font-bold text-hansu-success">SIM</span>
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span>Gestão Licenças</span>
                    <span className={cn("font-bold", level === 'Administrador' ? 'text-hansu-success' : 'text-hansu-error')}>
                      {level === 'Administrador' ? 'SIM' : 'NÃO'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

function cn(...inputs: any[]) {
  return inputs.filter(Boolean).join(' ');
}
