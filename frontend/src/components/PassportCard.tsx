import React from 'react';
import { QrCode, ShieldCheck, Download, Printer, ExternalLink } from 'lucide-react';

interface PassportCardProps {
  passportCode: string;
  eventCode: string;
  category: string;
  weightKg: number;
  riskLevel: string;
  status: string;
  evidenceHash: string;
  createdAt: string;
}

export const PassportCard: React.FC<PassportCardProps> = ({
  passportCode,
  eventCode,
  category,
  weightKg,
  riskLevel,
  status,
  evidenceHash,
  createdAt
}) => {
  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col gap-5 relative overflow-hidden shadow-2xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <QrCode className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-base text-slate-100 font-mono tracking-tight">{passportCode}</h3>
            <p className="text-xs text-slate-400">Digital Waste Passport & Tamper-Evident Chain Record</p>
          </div>
        </div>
        <span className="text-[10px] font-mono uppercase bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full border border-emerald-500/20 font-bold flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5" />
          {status}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-3 font-mono text-xs">
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
            <span className="text-slate-500 uppercase tracking-widest text-[10px]">Event ID</span>
            <span className="text-slate-200 font-bold">{eventCode}</span>
          </div>
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
            <span className="text-slate-500 uppercase tracking-widest text-[10px]">Verified Category</span>
            <span className="text-cyan-400 font-bold">{category}</span>
          </div>
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
            <span className="text-slate-500 uppercase tracking-widest text-[10px]">Mass Weight</span>
            <span className="text-emerald-400 font-bold">{weightKg} kg</span>
          </div>
        </div>

        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex items-center justify-center">
          <img 
            src={`/api/passports/${passportCode}/qr`} 
            alt="Passport QR Code" 
            className="w-32 h-32 bg-slate-950 p-2 rounded-lg border border-slate-800"
            onError={(e) => {
              // Fallback placeholder if API offline
              e.currentTarget.src = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100' fill='%2306B6D4'><rect width='100' height='100' fill='%230F172A'/><text x='50' y='50' fill='%2306B6D4' text-anchor='middle'>QR</text></svg>";
            }}
          />
        </div>
      </div>

      <!-- Audit Hash Footer -->
      <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-[11px] font-mono flex items-center justify-between text-slate-400">
        <span className="truncate max-w-[300px]">Audit Hash: <strong class="text-cyan-400 font-normal">{evidenceHash}</strong></span>
        <span className="text-slate-500 text-[10px]">{new Date(createdAt).toLocaleDateString()}</span>
      </div>

      <div className="flex gap-3">
        <button className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold py-2.5 rounded-xl border border-slate-700 flex items-center justify-center gap-2 transition">
          <Printer className="w-4 h-4 text-slate-400" />
          Print Passport Tag
        </button>
        <button className="flex-1 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 text-xs font-semibold py-2.5 rounded-xl border border-cyan-500/30 flex items-center justify-center gap-2 transition">
          <Download className="w-4 h-4 text-cyan-400" />
          Export PDF
        </button>
      </div>
    </div>
  );
};
