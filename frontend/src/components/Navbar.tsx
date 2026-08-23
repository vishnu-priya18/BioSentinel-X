import React from 'react';
import { ShieldCheck, User, LogOut, Bell, Zap } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const { userRole, userName, setUserRole, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-40 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div 
          onClick={() => navigate('/dashboard')}
          className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center cursor-pointer shadow-lg shadow-cyan-500/20"
        >
          <ShieldCheck className="w-5 h-5 text-slate-950" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-base tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              BioSentinel-X
            </h1>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-semibold">
              SIH 2026 Prototype
            </span>
          </div>
          <p className="text-[11px] text-slate-400">Software-Defined Biomedical Waste Decision OS</p>
        </div>
      </div>

      <!-- Quick Role Switcher for SIH Demo -->
      <div className="flex items-center gap-4">
        <button 
          onClick={() => navigate('/simulation')}
          className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs px-3.5 py-1.5 rounded-xl shadow-lg shadow-cyan-500/20 flex items-center gap-1.5 transition"
        >
          <Zap className="w-3.5 h-3.5 fill-slate-950" />
          Launch Grand Finale Demo
        </button>

        <div className="flex items-center gap-2 bg-slate-800/80 px-3 py-1.5 rounded-xl border border-slate-700/80 text-xs">
          <span className="text-slate-400">Role:</span>
          <select 
            value={userRole} 
            onChange={(e) => setUserRole(e.target.value as any)}
            className="bg-transparent text-cyan-300 font-bold font-mono focus:outline-none cursor-pointer"
          >
            <option value="ADMIN" className="bg-slate-900">ADMIN</option>
            <option value="SUPERVISOR" className="bg-slate-900">SUPERVISOR</option>
            <option value="SANITATION_WORKER" className="bg-slate-900">SANITATION_WORKER</option>
            <option value="VERIFIER" className="bg-slate-900">VERIFIER</option>
            <option value="VIEWER" className="bg-slate-900">VIEWER</option>
          </select>
        </div>

        <div className="flex items-center gap-2 text-xs text-slate-300">
          <User className="w-4 h-4 text-slate-400" />
          <span className="font-medium hidden sm:inline-block">{userName}</span>
        </div>

        <button onClick={logout} className="p-1.5 text-slate-400 hover:text-rose-400 transition">
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
