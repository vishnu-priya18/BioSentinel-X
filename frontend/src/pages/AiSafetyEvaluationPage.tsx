import React from 'react';
import { ShieldCheck, Cpu } from 'lucide-react';

export const AiSafetyEvaluationPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
            AI Safety Evaluation & Operational Coverage Metrics
          </h2>
          <p className="text-xs text-slate-400">
            Clearly distinguishing raw model classification accuracy from operational decision safety metrics.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Model Performance Column -->
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-slate-400" />
              Raw Model Performance Metrics
            </h3>
            <span className="text-[10px] font-mono bg-slate-800 text-slate-400 px-2 py-0.5 rounded">MobileNetV4</span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
              <span className="text-slate-500">Classification Accuracy:</span>
              <span className="font-bold text-slate-200">94.2%</span>
            </div>
            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
              <span className="text-slate-500">Precision / Recall / F1:</span>
              <span className="font-bold text-cyan-400">93.8% / 94.5% / 94.1%</span>
            </div>
            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
              <span className="text-slate-500">Expected Calibration Error:</span>
              <span className="font-bold text-purple-400">0.038 (Calibrated)</span>
            </div>
          </div>
        </div>

        <!-- Operational Safety Column -->
        <div className="glass-panel p-6 rounded-2xl border border-cyan-500/30 bg-cyan-950/20 space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="font-bold text-sm text-cyan-300 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-cyan-400" />
              Operational Safety Performance
            </h3>
            <span className="text-[10px] font-mono bg-cyan-500/20 text-cyan-300 px-2 py-0.5 rounded font-bold">Policy Engine</span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
              <span className="text-slate-400">Abstention Rate:</span>
              <span className="font-bold text-amber-400">18.4% (Safety Abstain)</span>
            </div>
            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
              <span className="text-slate-400">Autonomous Coverage:</span>
              <span className="font-bold text-emerald-400">81.6% (Safe Automation)</span>
            </div>
            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
              <span className="text-slate-400">False Acceptance Rate (FAR):</span>
              <span className="font-bold text-emerald-400 font-extrabold">0.2% (Target &lt; 0.5%)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
