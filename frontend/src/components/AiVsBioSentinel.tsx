import React from 'react';
import { ArrowRight, AlertTriangle, ShieldCheck, Cpu } from 'lucide-react';

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
            Demonstrating why raw AI confidence does NOT equal operational decision safety.
          </p>
        </div>
        <span className="text-[10px] font-mono uppercase bg-cyan-500/10 text-cyan-400 px-3 py-1 rounded-full border border-cyan-500/20 font-bold">
          SIH Key Thesis Comparison
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
              <span className="w-2 h-2 rounded-full bg-slate-500"></span>
              Conventional Image Classifier
            </h3>

            <div className="space-y-3 font-mono text-xs">
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-400">
                1. Image Capture <span className="text-slate-500">→ Waste Bag Photo</span>
              </div>
              <div className="flex justify-center"><ArrowRight className="w-4 h-4 text-slate-600 rotate-90" /></div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-400">
                2. CNN Classifier <span className="text-slate-500">→ MobileNet / ResNet</span>
              </div>
              <div className="flex justify-center"><ArrowRight className="w-4 h-4 text-slate-600 rotate-90" /></div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-cyan-400 font-bold">
                3. Raw Output <span className="text-slate-300">→ RED (91% Confidence)</span>
              </div>
              <div className="flex justify-center"><ArrowRight className="w-4 h-4 text-slate-600 rotate-90" /></div>
              <div className="bg-rose-950/60 border border-rose-500/40 p-3 rounded-lg text-rose-300 font-bold flex items-center justify-between">
                <span>4. ACTION TAKEN</span>
                <span className="text-xs uppercase bg-rose-500/20 px-2 py-0.5 rounded border border-rose-500/30">BLINDLY COLLECT</span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800 text-[11px] text-slate-500">
            ⚠ <strong>Critical Vulnerability:</strong> Blindly trusts 91% confidence despite container being opaque!
          </div>
        </div>

        <!-- BioSentinel-X Right Column -->
        <div className="bg-gradient-to-b from-cyan-950/40 to-slate-900 border border-cyan-500/30 p-5 rounded-xl flex flex-col justify-between relative overflow-hidden shadow-xl shadow-cyan-500/5">
          <div className="absolute top-0 right-0 bg-cyan-500 text-slate-950 text-[10px] font-mono font-bold px-3 py-1 rounded-bl-xl">
            BIOSENTINEL-X ENGINE
          </div>

          <div>
            <h3 className="font-bold text-sm text-cyan-300 mb-4 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-cyan-400" />
              Uncertainty-Aware Decision System
            </h3>

            <div className="space-y-2.5 font-mono text-xs">
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-slate-300 flex items-center justify-between">
                <span>1. Multi-Evidence Capture</span>
                <span className="text-[10px] text-cyan-400">Image, Barcode, Weight</span>
              </div>
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-slate-300 flex items-center justify-between">
                <span>2. AI Raw Prediction</span>
                <span className="text-[10px] text-slate-400">RED (91% Confidence)</span>
              </div>
              <div className="bg-amber-950/60 border border-amber-500/40 p-2.5 rounded-lg text-amber-300 flex items-center justify-between font-bold">
                <span>3. Content Observability</span>
                <span className="text-[10px] bg-amber-500/20 px-2 py-0.5 rounded border border-amber-500/30">CONTAINER OPAQUE!</span>
              </div>
              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-slate-300 flex items-center justify-between">
                <span>4. Uncertainty H(x)</span>
                <span className="text-[10px] text-rose-400 font-bold">SPORTS HIGH UNCERTAINTY</span>
              </div>
              <div className="bg-emerald-950/80 border border-emerald-500/50 p-3 rounded-lg text-emerald-300 font-bold flex items-center justify-between shadow-lg">
                <span className="flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  5. DETERMINISTIC DECISION
                </span>
                <span className="text-xs uppercase bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/40 font-bold">
                  UNKNOWN / HUMAN REVIEW
                </span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-cyan-500/20 text-[11px] text-cyan-300/80 font-medium">
            ✓ <strong>Safety Guarantee:</strong> Separates prediction from permission to act. Abstains when evidence is insufficient.
          </div>
        </div>
      </div>

      <!-- Signature Statement Bottom Banner -->
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl text-center">
        <p className="text-sm font-semibold text-slate-200">
          "Confidence answers <em className="text-cyan-400 font-serif font-normal">'How sure is the model?'</em>. BioSentinel-X asks <em className="text-emerald-400 font-serif font-normal">'Is it safe to act?'</em>"
        </p>
      </div>
    </div>
  );
};
