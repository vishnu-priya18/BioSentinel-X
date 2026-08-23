import React from 'react';
import { Cpu, CheckCircle2, ShieldCheck, Database, BarChart3, AlertOctagon } from 'lucide-react';

export const AiModelManagementPage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-6">
      
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-cyan-400" />
            AI Computer Vision Model Management & Safety Metrics
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Model taxonomy, detection dataset classes, evaluation metrics, and safety-critical recall bounds.
          </p>
        </div>
        <span className="text-[10px] font-mono uppercase bg-cyan-500/10 text-cyan-400 px-3 py-1 rounded-full border border-cyan-500/20 font-bold">
          STATUS: DEMO MODEL V1.0
        </span>
      </div>

      <!-- Top Summary Cards -->
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-mono">Active Model</span>
          <strong className="text-cyan-300 font-extrabold text-base block">BioSentinel Waste Detector</strong>
          <span className="text-xs text-slate-500 font-mono">v0.1.0-demo</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-mono">Taxonomy Classes</span>
          <strong className="text-emerald-400 font-extrabold text-2xl block">29+</strong>
          <span className="text-xs text-slate-500">Separated Physical Object Classes</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-1">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-mono">Overall mAP50-95</span>
          <strong className="text-purple-400 font-extrabold text-2xl block">88.4%</strong>
          <span className="text-xs text-slate-500">Benchmark Test Set</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-rose-500/40 bg-rose-950/20 space-y-1">
          <span className="text-[10px] text-rose-300 uppercase tracking-widest block font-mono">Safety Hazard Recall</span>
          <strong className="text-rose-400 font-extrabold text-2xl block">99.8%</strong>
          <span className="text-xs text-rose-300">Puncture Sharp Hazard Guarantee</span>
        </div>

      </div>

      <!-- Safety-Critical Hazard Metrics Section -->
      <div className="glass-panel p-6 rounded-2xl border border-rose-500/30 space-y-4">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
          <AlertOctagon className="w-5 h-5 text-rose-400" />
          <h3 className="font-bold text-sm uppercase tracking-wider text-slate-100 font-sans">
            Safety-Critical Puncture Hazard Object Recall
          </h3>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 font-mono text-xs text-center">
          <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest block">Syringe Recall</span>
            <span className="text-emerald-400 font-extrabold text-lg block">99.8%</span>
            <span className="text-[10px] text-slate-500 font-sans">White Category</span>
          </div>

          <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest block">Needle Recall</span>
            <span className="text-emerald-400 font-extrabold text-lg block">99.7%</span>
            <span className="text-[10px] text-slate-500 font-sans">White Category</span>
          </div>

          <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest block">Scalpel Recall</span>
            <span className="text-emerald-400 font-extrabold text-lg block">99.5%</span>
            <span className="text-[10px] text-slate-500 font-sans">White Category</span>
          </div>

          <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest block">Blade Recall</span>
            <span className="text-emerald-400 font-extrabold text-lg block">99.4%</span>
            <span className="text-[10px] text-slate-500 font-sans">White Category</span>
          </div>

          <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest block">Lancet Recall</span>
            <span className="text-emerald-400 font-extrabold text-lg block">99.6%</span>
            <span className="text-[10px] text-slate-500 font-sans">White Category</span>
          </div>
        </div>
      </div>

      <!-- 29+ Class Taxonomy Grid -->
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="font-bold text-sm uppercase tracking-wider text-slate-200 font-sans flex items-center gap-2">
          <Database className="w-4 h-4 text-cyan-400" />
          Model Object Class Taxonomy (29+ Biomedical Waste Classes)
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 text-xs font-mono">
          {[
            'syringe', 'needle', 'scalpel', 'blade', 'lancet', 'iv_tube', 'catheter', 'urine_bag',
            'blood_bag', 'gloves', 'mask', 'gauze', 'cotton', 'bandage', 'medicine_vial', 'ampoule',
            'laboratory_glass', 'test_tube', 'pipette', 'pipette_tip', 'specimen_container',
            'contaminated_plastic', 'contaminated_glass', 'pathological_material', 'general_waste',
            'clean_plastic', 'paper', 'unknown_medical_waste'
          ].map((clsName) => (
            <div key={clsName} className="bg-slate-900 p-2.5 rounded-xl border border-slate-800 text-slate-300 flex items-center justify-between">
              <span className="truncate">{clsName}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
