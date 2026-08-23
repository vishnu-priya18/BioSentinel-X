import React from 'react';
import { AlertTriangle } from 'lucide-react';

export const SafetyDisclaimerBanner: React.FC = () => {
  return (
    <div className="bg-amber-500/10 border border-amber-500/30 text-amber-300 px-4 py-2.5 rounded-xl text-xs flex items-center justify-between shadow-sm">
      <div className="flex items-center gap-2.5">
        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
        <span className="font-medium">
          <strong className="font-bold text-amber-200">Mandatory Safety Policy:</strong> AI classification is decision support and does not replace trained biomedical-waste personnel, hospital protocols, or applicable regulatory requirements.
        </span>
      </div>
      <span className="text-[10px] font-mono bg-amber-500/20 px-2 py-0.5 rounded border border-amber-500/30 text-amber-200 uppercase tracking-widest shrink-0 hidden md:inline-block">
        Uncertainty-Aware Core
      </span>
    </div>
  );
};
