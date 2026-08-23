import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, Scan, CheckSquare, Truck, QrCode, Compass, 
  BrainCircuit, Activity, AlertTriangle, BarChart3, ShieldCheck, 
  History, PlayCircle, Users, Building2, Tags, FileText, Settings, User
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/scan', label: 'Scan Waste (Mobile PWA)', icon: Scan, highlight: true },
    { to: '/verification', label: 'Verification Queue', icon: CheckSquare },
    { to: '/collection', label: 'Collection Tasks', icon: Truck },
    { to: '/passports', label: 'Waste Passports', icon: QrCode },
    { to: '/evidence', label: 'Evidence Explorer', icon: Compass },
    { to: '/ai-vs-biosentinel', label: 'AI vs BioSentinel-X', icon: BrainCircuit },
    { to: '/intelligence', label: 'Waste Intelligence', icon: Activity },
    { to: '/digital-twin', label: 'Digital Twin', icon: Building2 },
    { to: '/analytics', label: 'Analytics', icon: BarChart3 },
    { to: '/ai-safety', label: 'AI Safety Evaluation', icon: ShieldCheck },
    { to: '/alerts', label: 'Alerts Feed', icon: AlertTriangle },
    { to: '/audit', label: 'Audit Trail (SHA-256)', icon: History },
    { to: '/simulation', label: 'Grand Finale Demo', icon: PlayCircle },
    { to: '/users', label: 'User Admin', icon: Users },
    { to: '/departments', label: 'Departments', icon: Building2 },
    { to: '/categories', label: 'Waste Categories', icon: Tags },
    { to: '/regulatory', label: 'CPCB Rules', icon: FileText },
    { to: '/settings', label: 'System Settings', icon: Settings },
    { to: '/profile', label: 'User Profile', icon: User },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/60 backdrop-blur hidden md:flex flex-col justify-between py-4 shrink-0">
      <div className="space-y-1 px-3 overflow-y-auto max-h-[calc(100vh-100px)]">
        <p className="px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">Main Navigation</p>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition ${
                  isActive
                    ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                } ${item.highlight ? 'ring-1 ring-cyan-500/30 text-cyan-300 font-bold' : ''}`
              }
            >
              <Icon className="w-4 h-4 shrink-0 text-cyan-400" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>
    </aside>
  );
};
