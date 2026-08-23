import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KpiCardProps {
  title: string;
  value: string | number;
  subtitle: string;
  icon: LucideIcon;
  colorHex?: string;
  trend?: string;
}

export const KpiCard: React.FC<KpiCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend
}) => {
  return (
    <div className="glass-panel p-4 rounded-2xl border border-slate-800 flex items-center justify-between transition hover:border-slate-700">
      <div>
        <p className="text-[10px] text-slate-400 uppercase tracking-widest font-semibold mb-1">{title}</p>
        <h4 className="font-mono text-2xl font-extrabold text-slate-100">{value}</h4>
        <p className="text-[11px] text-slate-500 mt-1">{subtitle}</p>
      </div>

      <div className="w-11 h-11 rounded-xl bg-slate-800/80 border border-slate-700/80 flex items-center justify-center text-cyan-400 shrink-0">
        <Icon className="w-5 h-5 text-cyan-400" />
      </div>
    </div>
  );
};
