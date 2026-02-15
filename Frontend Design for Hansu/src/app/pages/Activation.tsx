import React, { useState } from "react";
import { motion } from "motion/react";
import { ShieldCheck, Key, FileText, CheckCircle2, AlertCircle, ArrowRight, Loader2 } from "lucide-react";
import { toast } from "sonner";

export const Activation = ({ onActivate }: { onActivate: () => void }) => {
  const [step, setStep] = useState<'upload' | 'verifying' | 'success'>('upload');
  const [licenseCode, setLicenseCode] = useState("");

  const handleActivate = () => {
    if (!licenseCode && step === 'upload') {
      toast.error("Por favor, insira o código ou anexe o arquivo .lic");
      return;
    }
    setStep('verifying');
    setTimeout(() => {
      setStep('success');
      toast.success("Licença validada com sucesso!");
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-hansu-bg flex items-center justify-center p-6 bg-[radial-gradient(circle_at_top_right,_var(--color-hansu-primary)_0%,_transparent_25%)]">
      <div className="max-w-md w-full">
        <div className="text-center mb-10">
          <div className="w-16 h-16 bg-hansu-primary rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl shadow-hansu-primary/20">
            <ShieldCheck className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-black text-hansu-text tracking-tight mb-2">HANSU HUB</h1>
          <p className="text-slate-500 font-medium">Ativação de Licença Digital</p>
        </div>

        <motion.div 
          layout
          className="bg-white p-8 rounded-2xl border border-hansu-border shadow-2xl relative overflow-hidden"
        >
          {step === 'upload' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
              <div>
                <label className="block text-sm font-bold text-hansu-neutral-dark mb-2">Código da Licença</label>
                <div className="relative">
                  <Key className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                  <input 
                    type="text" 
                    value={licenseCode}
                    onChange={(e) => setLicenseCode(e.target.value)}
                    placeholder="XXXX-XXXX-XXXX-XXXX"
                    className="w-full pl-10 pr-4 py-3 border border-hansu-border rounded-xl focus:ring-2 focus:ring-hansu-primary/20 focus:outline-none font-mono"
                  />
                </div>
              </div>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-slate-100" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-white px-2 text-slate-400 font-bold">ou anexe arquivo</span>
                </div>
              </div>

              <div className="border-2 border-dashed border-slate-200 rounded-xl p-8 text-center hover:border-hansu-primary transition-colors cursor-pointer group">
                <FileText className="w-8 h-8 text-slate-300 mx-auto mb-2 group-hover:text-hansu-primary" />
                <span className="text-xs font-bold text-slate-500 block">ARRASTE ARQUIVO .LIC</span>
              </div>

              <button 
                onClick={handleActivate}
                className="w-full py-4 bg-hansu-primary text-white font-bold rounded-xl shadow-lg shadow-hansu-primary/20 hover:bg-hansu-primary-hover transition-all flex items-center justify-center gap-2"
              >
                Ativar Sistema <ArrowRight className="w-4 h-4" />
              </button>
            </motion.div>
          )}

          {step === 'verifying' && (
            <div className="py-12 text-center space-y-4">
              <Loader2 className="w-12 h-12 text-hansu-primary animate-spin mx-auto" />
              <div className="text-lg font-bold text-hansu-text">Validando Assinatura Digital...</div>
              <p className="text-sm text-slate-500">Isso pode levar alguns segundos.</p>
            </div>
          )}

          {step === 'success' && (
            <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="py-8 text-center space-y-6">
              <div className="w-20 h-20 bg-green-50 rounded-full flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-12 h-12 text-hansu-success" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-hansu-text">Licença Ativada!</h3>
                <p className="text-slate-500 mt-2">Sua chave Hansu Enterprise é válida até 15/02/2027.</p>
              </div>
              <div className="bg-slate-50 p-4 rounded-xl text-left border border-slate-100">
                <div className="text-[10px] font-bold text-slate-400 uppercase mb-2">Permissões Habilitadas</div>
                <ul className="text-xs font-bold text-hansu-neutral-dark space-y-2">
                  <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-hansu-success rounded-full" /> Acesso ao Hub Completo</li>
                  <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-hansu-success rounded-full" /> Extração Ecac / EFD / ICMS</li>
                  <li className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-hansu-success rounded-full" /> Editor de Registros SPED</li>
                </ul>
              </div>
              <button 
                onClick={onActivate}
                className="w-full py-4 bg-hansu-neutral-dark text-white font-bold rounded-xl hover:bg-slate-800 transition-all"
              >
                Ir para o Hub
              </button>
            </motion.div>
          )}
        </motion.div>
        
        <div className="mt-8 text-center">
          <p className="text-xs text-slate-400 font-medium">Hansu v2.4.0 — Sistema de Inteligência Fiscal</p>
          <p className="text-xs text-slate-400">© 2026 Hansu Tecnologia. Todos os direitos reservados.</p>
        </div>
      </div>
    </div>
  );
};
