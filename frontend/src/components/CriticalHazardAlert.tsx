import React from 'react';
import { AlertOctagon, ShieldAlert, XCircle } from 'lucide-react';
import { HazardAssessment } from '../types';

interface CriticalHazardAlertProps {
  hazard: HazardAssessment;
  aiConfidence?: number;
}

export const CriticalHazardAlert: React.FC<CriticalHazardAlertProps> = ({ hazard, aiConfidence = 0.97 }) => {
  if (!hazard || !hazard.detected) return null;

  return (
    <div className="glass-panel p-5 rounded-2xl border-2 border-rose-500/60 bg-rose-950/30 space-y-4 shadow-2xl shadow-rose-950/50">
      <div className="flex items-center justify-between border-b border-rose-500/30 pb-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-rose-500/20 border border-rose-500/50 flex items-center justify-center text-rose-400 font-extrabold animate-pulse">
            <AlertOctagon className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-extrabold text-base text-rose-200 tracking-wide flex items-center gap-2">
              ⚠ CRITICAL HAZARD DETECTED
            </h3>
            <p className="text-xs text-rose-300 font-mono">
              Hazard Object: <span className="font-extrabold underline text-rose-100">{hazard.hazard_type}</span>
            </p>
          </div>
        </div>

        <div className="text-right">
          <span className="text-[10px] bg-rose-500/30 text-rose-300 px-3 py-1 rounded-lg font-mono font-extrabold border border-rose-500/40 uppercase tracking-wider block">
            SEVERITY: {hazard.severity}
          </span>
          <span className="text-[11px] text-rose-400 font-mono block mt-1">
            Hazard Score: {(hazard.score * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 font-mono text-xs">
        <div className="bg-slate-900/90 p-3 rounded-xl border border-rose-500/30 space-y-1">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-sans">Raw AI Prediction Confidence</span>
          <span className="text-cyan-300 font-extrabold text-sm">{ (aiConfidence * 100).toFixed(1) }%</span>
          <p className="text-[10px] text-slate-500 font-sans">Visual Classifier Probability</p>
        </div>

        <div className="bg-rose-900/30 p-3 rounded-xl border border-rose-500/50 space-y-1">
          <span className="text-[10px] text-rose-300 uppercase tracking-widest block font-sans">Automation Permission</span>
          <span className="text-rose-400 font-extrabold text-sm flex items-center gap-1">
            <XCircle className="w-4 h-4 text-rose-400 inline" />
            BLOCKED BY SAFETY POLICY
          </span>
          <p className="text-[10px] text-rose-300 font-sans">High AI confidence does NOT override a sharp hazard.</p>
        </div>
      </div>

      <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800 text-xs font-sans text-slate-300 flex items-start gap-2">
        <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
        <p>
          <strong className="text-slate-100 font-mono">Safety Explanation:</strong> {hazard.explanation}
        </p>
      </div>
    </div>
  );
};
