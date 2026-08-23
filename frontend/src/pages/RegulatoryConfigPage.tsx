import React from 'react';
import { FileText } from 'lucide-react';

export const RegulatoryConfigPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <FileText className="w-5 h-5 text-cyan-400" />
            Regulatory Rules & Jurisdiction Mapping
          </h2>
          <p className="text-xs text-slate-400">
            Compliance-supporting workflow configuration for India CPCB 2016 guidelines.
          </p>
        </div>
      </div>

      <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-2 text-xs font-mono">
          <div className="flex justify-between text-cyan-400 font-bold">
            <span>RULE-CPCB-001 (Yellow Incineration)</span>
            <span>Max Storage: 48 hrs</span>
          </div>
          <p className="text-slate-300 font-sans">Anatomical waste, soiled cotton, chemical waste. Mandates CPCB barcode tag scanning before pickup.</p>
        </div>

        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-2 text-xs font-mono">
          <div className="flex justify-between text-cyan-400 font-bold">
            <span>RULE-CPCB-002 (Red Autoclave/Recycle)</span>
            <span>Max Storage: 48 hrs</span>
          </div>
          <p className="text-slate-300 font-sans">Contaminated plastic tubing, IV bottles, catheters. Must undergo autoclave shredding before recycling.</p>
        </div>
      </div>
    </div>
  );
};
