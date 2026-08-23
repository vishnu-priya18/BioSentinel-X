import React from 'react';
import { X, Calculator, CheckCircle2 } from 'lucide-react';

interface ExplainScoreModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  score: number;
  breakdown: Record<string, number>;
  weightedContributions: Record<string, number>;
  formulaExplanation: string;
}

export const ExplainScoreModal: React.FC<ExplainScoreModalProps> = ({
  isOpen,
  onClose,
  title,
  score,
  breakdown,
  weightedContributions,
  formulaExplanation
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Calculator className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-base text-slate-100">{title}</h3>
            <p className="text-xs text-slate-400">Mathematical Breakdown & Weighted Component Analysis</p>
          </div>
        </div>

        <!-- Total Calculated Score -->
        <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 mb-5 text-center">
          <span className="text-[10px] text-slate-500 uppercase tracking-widest block mb-1">Calculated Priority Score</span>
          <div className="font-mono text-4xl font-extrabold text-cyan-400">{score.toFixed(1)}</div>
          <span className="text-xs text-slate-400 font-mono mt-1 block">Scale: 0.0 - 100.0</span>
        </div>

        <!-- Formula Explanation -->
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-3 mb-5 text-xs font-mono text-cyan-300">
          <strong className="text-slate-300 block mb-1 font-sans text-[11px] uppercase tracking-wider">Formula Used:</strong>
          {formulaExplanation}
        </div>

        <!-- Weighted Contributions Table -->
        <div className="space-y-2 mb-6">
          <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Weighted Contribution Breakdown:</h4>
          {Object.keys(breakdown).map((key) => (
            <div key={key} className="bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-300 capitalize">{key.replace('_', ' ')}</span>
              <div className="flex items-center gap-3">
                <span className="text-slate-500 text-[11px]">Raw: {breakdown[key]}</span>
                <span className="text-cyan-400 font-bold">+{weightedContributions[key]} pts</span>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={onClose}
          className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs py-2.5 rounded-xl border border-slate-700 transition"
        >
          Close Explanation
        </button>
      </div>
    </div>
  );
};
