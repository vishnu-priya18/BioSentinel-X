import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, ShieldAlert } from 'lucide-react';
import { DecisionState } from '../types';

interface ReasoningItem {
  status: 'PASS' | 'WARNING' | 'FAIL';
  source: string;
  message: string;
  technical_value: string;
  explanation: string;
}

interface WhyNotPanelProps {
  predictedCategory: string;
  confidence: number;
  decisionState: DecisionState;
  reasons: ReasoningItem[];
}

export const WhyNotPanel: React.FC<WhyNotPanelProps> = ({
  predictedCategory,
  confidence,
  decisionState,
  reasons
}) => {
  const getBadgeStyle = (state: DecisionState) => {
    switch (state) {
      case 'SAFE_TO_AUTOMATE':
        return 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400';
      case 'NEEDS_VERIFICATION':
        return 'bg-amber-500/10 border-amber-500/30 text-amber-400';
      case 'HIGH_RISK_ESCALATION':
      case 'UNKNOWN':
        return 'bg-rose-500/10 border-rose-500/30 text-rose-400';
      default:
        return 'bg-slate-800 text-slate-300';
    }
  };

  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
        <div className="flex items-center gap-2.5">
          <ShieldAlert className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-sm uppercase tracking-wider text-slate-200">
            "Why Not?" Decision Reasoning Panel
          </h3>
        </div>
        <span className={`text-[10px] font-mono font-bold px-2.5 py-1 rounded-full border ${getBadgeStyle(decisionState)}`}>
          {decisionState}
        </span>
      </div>

      <!-- AI Prediction Header -->
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5 flex items-center justify-between">
        <div>
          <span className="text-[10px] text-slate-400 uppercase tracking-widest block">AI Model Raw Prediction</span>
          <span className="font-mono text-base font-bold text-cyan-400">{predictedCategory.toUpperCase()}</span>
        </div>
        <div className="text-right">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-sans">Raw Confidence</span>
          <span className="font-mono text-sm font-bold text-slate-200">{(confidence * 100).toFixed(1)}%</span>
        </div>
      </div>

      <div className="bg-amber-500/10 border border-amber-500/20 rounded-xl p-3 text-xs text-amber-300 font-sans flex items-start gap-2">
        <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
        <p>
          <strong className="font-mono text-amber-200">AI Safety Rule:</strong> High AI prediction confidence describes probability, NOT operational permission to act.
        </p>
      </div>

      <!-- Reasoning Table -->
      <div className="space-y-2">
        {reasons.map((item, idx) => (
          <div key={idx} className="bg-slate-900/80 border border-slate-800/80 rounded-xl p-3 flex items-start gap-3 transition hover:border-slate-700">
            {item.status === 'PASS' && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />}
            {item.status === 'WARNING' && <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />}
            {item.status === 'FAIL' && <XCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />}
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2 mb-0.5">
                <span className="text-xs font-semibold text-slate-200">{item.source}</span>
                <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${
                  item.status === 'PASS' ? 'bg-emerald-500/10 text-emerald-400' : 
                  item.status === 'WARNING' ? 'bg-amber-500/10 text-amber-400' : 'bg-rose-500/10 text-rose-400'
                }`}>
                  {item.technical_value}
                </span>
              </div>
              <p className="text-xs text-slate-300 font-medium mb-0.5">{item.message}</p>
              <p className="text-[11px] text-slate-500">{item.explanation}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
