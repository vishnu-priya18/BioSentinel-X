import React from 'react';
import { User, ShieldCheck } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const ProfilePage: React.FC = () => {
  const { userName, userRole } = useAuth();

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
          <User className="w-5 h-5 text-cyan-400" />
          User Profile
        </h2>
      </div>

      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-bold text-xl">
            {userName.charAt(0)}
          </div>
          <div>
            <h3 className="font-bold text-base text-slate-100">{userName}</h3>
            <p className="text-xs text-slate-400 font-mono">Assigned Role: <strong className="text-cyan-400">{userRole}</strong></p>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800 space-y-2 text-xs font-mono">
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
            <span className="text-slate-500">Hospital Assignment:</span>
            <span className="text-slate-200">Sentinel General Hospital</span>
          </div>
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
            <span className="text-slate-500">Session Status:</span>
            <span className="text-emerald-400 font-bold">AUTHENTICATED (JWT Active)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
