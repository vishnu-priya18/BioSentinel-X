import React from 'react';
import { Tags } from 'lucide-react';

export const WasteCategoryManagementPage: React.FC = () => {
  const cats = [
    { code: 'Yellow', name: 'Yellow (Incineration)', color: '#F59E0B', desc: 'Anatomical waste, soiled linen, chemical waste' },
    { code: 'Red', name: 'Red (Autoclave/Recycle)', color: '#EF4444', desc: 'Contaminated plastic tubing, IV bottles, catheters' },
    { code: 'White', name: 'White Sharps', color: '#F8FAFC', desc: 'Needles, scalpels, blades in puncture-proof container' },
    { code: 'Blue', name: 'Blue Glassware', color: '#3B82F6', desc: 'Glass bottles, medicine vials, metallic implants' },
    { code: 'Unknown', name: 'Unknown / Unsafe', color: '#64748B', desc: 'Uncertain or unobservable waste content' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Tags className="w-5 h-5 text-cyan-400" />
            Configurable Biomedical Waste Categories
          </h2>
          <p className="text-xs text-slate-400">
            Category rules, safety notes, and accepted examples configured dynamically per hospital workflow.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cats.map((c) => (
          <div key={c.code} className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-sm text-slate-100">{c.name}</h3>
              <span className="w-3 h-3 rounded-full" style={{ backgroundColor: c.color }}></span>
            </div>
            <p className="text-xs text-slate-400 font-medium">{c.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
