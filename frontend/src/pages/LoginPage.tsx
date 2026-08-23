import React, { useState } from 'react';
import { ShieldCheck, Lock, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { UserRole } from '../types';

export const LoginPage: React.FC = () => {
  const { setUserRole, setUserName } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('supervisor@sentinel.org');

  const handleDemoLogin = (role: UserRole, name: string) => {
    setUserRole(role);
    setUserName(name);
    if (role === 'SANITATION_WORKER') {
      navigate('/scan');
    } else {
      navigate('/dashboard');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950">
      <div className="glass-panel p-8 rounded-3xl border border-slate-800 max-w-md w-full space-y-6 shadow-2xl">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-slate-950 mx-auto shadow-lg shadow-cyan-500/20">
            <ShieldCheck className="w-7 h-7" />
          </div>
          <h1 className="font-extrabold text-2xl text-slate-100">BioSentinel-X</h1>
          <p className="text-xs text-slate-400">Software-Defined Biomedical Waste Decision OS</p>
        </div>

        <div className="space-y-3 font-mono text-xs">
          <p className="text-slate-400 font-sans uppercase tracking-widest text-[10px] text-center font-semibold">Select SIH Demo Role Account:</p>

          <button 
            onClick={() => handleDemoLogin('ADMIN', 'Dr. Rajesh Sharma (Admin)')}
            className="w-full bg-slate-900 hover:bg-slate-800 p-3 rounded-xl border border-slate-800 text-left font-bold text-slate-200 flex justify-between items-center transition"
          >
            <span>ADMIN Account</span>
            <span className="text-[10px] bg-purple-500/10 text-purple-400 px-2 py-0.5 rounded border border-purple-500/20">FULL ACCESS</span>
          </button>

          <button 
            onClick={() => handleDemoLogin('SUPERVISOR', 'Anita Roy (Supervisor)')}
            className="w-full bg-slate-900 hover:bg-slate-800 p-3 rounded-xl border border-slate-800 text-left font-bold text-cyan-300 flex justify-between items-center transition ring-1 ring-cyan-500/30"
          >
            <span>SUPERVISOR Account</span>
            <span className="text-[10px] bg-cyan-500/10 text-cyan-400 px-2 py-0.5 rounded border border-cyan-500/20">COMMAND CENTER</span>
          </button>

          <button 
            onClick={() => handleDemoLogin('SANITATION_WORKER', 'Staff Worker #412')}
            className="w-full bg-slate-900 hover:bg-slate-800 p-3 rounded-xl border border-slate-800 text-left font-bold text-emerald-300 flex justify-between items-center transition"
          >
            <span>SANITATION WORKER Account</span>
            <span className="text-[10px] bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded border border-emerald-500/20">MOBILE PWA</span>
          </button>

          <button 
            onClick={() => handleDemoLogin('VERIFIER', 'Safety Verifier Vikram')}
            className="w-full bg-slate-900 hover:bg-slate-800 p-3 rounded-xl border border-slate-800 text-left font-bold text-amber-300 flex justify-between items-center transition"
          >
            <span>SAFETY VERIFIER Account</span>
            <span className="text-[10px] bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded border border-amber-500/20">VERIFY QUEUE</span>
          </button>
        </div>

        <p className="text-[11px] text-slate-500 text-center">
          "Don't just classify the waste. Know what you don't know."
        </p>
      </div>
    </div>
  );
};
