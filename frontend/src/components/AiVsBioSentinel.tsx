import React from 'react';
import { ArrowRight, AlertTriangle, ShieldCheck, Cpu, XCircle, AlertOctagon } from 'lucide-react';

export const AiVsBioSentinel: React.FC = () => {
  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col gap-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-cyan-400" />
            AI vs BioSentinel-X Architecture Comparison
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Same AI prediction. Different safety decision. Because raw AI confidence is NOT permission to act.
          </p>
        </div>
        <span className="text-[10px] font-mono uppercase bg-cyan-500/10 text-cyan-400 px-3 py-1 rounded-full border border-cyan-500/20 font-bold">
          SIH Killer Innovation Demo
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Traditional AI Left Column -->
        <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-xl flex flex-col justify-between relative overflow-hidden">
          <div className="absolute top-0 right-0 bg-slate-800 text-slate-400 text-[10px] font-mono font-bold px-3 py-1 rounded-bl-xl border-l border-b border-slate-700">
            TRADITIONAL AI
          </div>

          <div>
            <h3 className="font-bold text-sm text-slate-300 mb-4 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-slate-500"></span>
              Conventional AI Classifier Workflow
            </h3>

            <div className="space-y-3 font-mono text-xs">
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-300">
                1. Input Image <span className="text-amber-400 font-bold">→ SYRINGE / SHARP</span>
              </div>
              <div className="flex justify-center"><ArrowRight className="w-4 h-4 text-slate-600 rotate-90" /></div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-cyan-400 font-bold">
                2. AI Prediction <span className="text-slate-200">→ WHITE (97% Confidence)</span>
              </div>
              <div className="flex justify-center"><ArrowRight className="w-4 h-4 text-slate-600 rotate-90" /></div>
              <div className="bg-emerald-950/60 border border-emerald-500/40 p-3 rounded-lg text-emerald-400 font-bold flex items-center justify-between">
                <span>3. OPERATIONAL DECISION</span>
                <span className="text-xs uppercase bg-emerald-500/20 px-2.5 py-1 rounded border border-emerald-500/30">🟢 GREEN / SAFE TO AUTOMATE</span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800 text-[11px] text-rose-400 flex items-start gap-2">
            <XCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
            <p>
              <strong>CRITICAL SAFETY FLAW:</strong> Equates 97% confidence with operational safety permission, authorizing automatic handling of a dangerous sharp!
            </p>
          </div>
        </div>

        <!-- BioSentinel-X Right Column -->
        <div className="bg-gradient-to-b from-cyan-950/40 to-slate-900 border border-cyan-500/30 p-5 rounded-xl flex flex-col justify-between relative overflow-hidden shadow-xl shadow-cyan-500/5">
          <div className="absolute top-0 right-0 bg-cyan-500 text-slate-950 text-[10px] font-mono font-bold px-3 py-1 rounded-bl-xl">
            BIOSENTINEL-X SAFETY ENGINE
          </div>

          <div>
            <h3 className="font-bold text-sm text-cyan-300 mb-4 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-cyan-400" />
              Safety Gate & Deterministic Policy Core
            </h3>

            <div className="space-y-2.5 font-mono text-xs">
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-slate-300 flex items-center justify-between">
                <span>1. Input Image</span>
                <span className="text-[10px] text-amber-400 font-bold">SYRINGE / SHARP</span>
              </div>
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-slate-300 flex items-center justify-between">
                <span>2. AI Prediction</span>
                <span className="text-[10px] text-slate-400">WHITE (97% Confidence)</span>
              </div>
              <div className="bg-rose-950/80 border border-rose-500/60 p-2.5 rounded-lg text-rose-300 flex items-center justify-between font-bold">
                <span className="flex items-center gap-1.5">
                  <AlertOctagon className="w-4 h-4 text-rose-400" />
                  3. Hazard Gate
                </span>
                <span className="text-[10px] bg-rose-500/30 text-rose-200 px-2 py-0.5 rounded border border-rose-500/40">CRITICAL SHARP DETECTED</span>
              </div>
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-slate-300 flex items-center justify-between">
                <span>4. Automation Gate</span>
                <span className="text-[10px] text-rose-400 font-extrabold">AUTOMATION BLOCKED</span>
              </div>
              <div className="bg-rose-950/90 border border-rose-500 p-3 rounded-lg text-rose-200 font-bold flex items-center justify-between shadow-lg">
                <span className="flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-rose-400" />
                  5. FINAL DECISION
                </span>
                <span className="text-xs uppercase bg-rose-500/30 text-rose-200 px-2.5 py-1 rounded border border-rose-500/50 font-extrabold">
                  🔴 HIGH_RISK_ESCALATION
                </span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-cyan-500/20 text-[11px] text-cyan-300/90 font-medium">
            ✓ <strong>Safety Principle:</strong> Separates prediction from permission to act. High AI confidence NEVER overrides a critical sharp hazard.
          </div>
        </div>
      </div>

      <!-- Signature Statement Bottom Banner -->
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl text-center space-y-1">
        <p className="text-base font-extrabold text-slate-100">
          "We don't build an AI that always gives an answer. We build a system that knows when an answer isn't safe enough to act on."
        </p>
      </div>
    </div>
  );
};
