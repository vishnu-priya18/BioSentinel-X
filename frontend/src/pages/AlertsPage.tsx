import React from 'react';
import { AlertTriangle } from 'lucide-react';

export const AlertsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            Hospital Alerts & Anomaly Feed
          </h2>
          <p className="text-xs text-slate-400">
            Real-time feed of detected volume surges, barcode mismatches, and high-risk abstentions.
          </p>
        </div>
      </div>

      <div className="space-y-3 font-mono text-xs">
        <div className="glass-panel p-4 rounded-xl border border-rose-500/40 bg-rose-950/20 space-y-1">
          <div className="flex justify-between text-rose-300 font-bold">
            <span>CRITICAL_WEIGHT_SURGE (Pathology Lab)</span>
            <span className="text-[10px] bg-rose-500/20 px-2 py-0.5 rounded">Z = +4.8</span>
          </div>
          <p className="text-slate-300 font-sans text-xs">DEMO-005 registered 18.5kg vs 2.1kg baseline (8.8x multiplier). Recommended supervisor review.</p>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-amber-500/40 bg-amber-950/20 space-y-1">
          <div className="flex justify-between text-amber-300 font-bold">
            <span>BARCODE_CATEGORY_MISMATCH (Ward A)</span>
            <span className="text-[10px] bg-amber-500/20 px-2 py-0.5 rounded">DEMO-004</span>
          </div>
          <p className="text-slate-300 font-sans text-xs">Yellow barcode tag placed on Red plastic tubing container.</p>
        </div>
      </div>
    </div>
  );
};
