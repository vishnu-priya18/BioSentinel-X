import React from 'react';
import { Building2 } from 'lucide-react';

export const DepartmentManagementPage: React.FC = () => {
  const depts = [
    { name: 'ICU Ward', code: 'ICU-01', baseline: 12.5, criticality: 95.0 },
    { name: 'Emergency Ward', code: 'EMG-01', baseline: 15.0, criticality: 90.0 },
    { name: 'Pathology Laboratory', code: 'LAB-01', baseline: 2.1, criticality: 85.0 },
    { name: 'Ward A', code: 'WDA-01', baseline: 8.0, criticality: 60.0 },
    { name: 'Operation Theatre', code: 'OT-01', baseline: 20.0, criticality: 98.0 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Building2 className="w-5 h-5 text-cyan-400" />
            Hospital Department Baseline Configuration
          </h2>
          <p className="text-xs text-slate-400">
            Daily baseline waste mass averages (kg) and criticality ratings for statistical z-score anomaly detection.
          </p>
        </div>
      </div>

      <div className="glass-panel p-5 rounded-2xl border border-slate-800">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400">
              <th className="py-2.5 px-3">Department Name</th>
              <th className="py-2.5 px-3">Code</th>
              <th className="py-2.5 px-3">Daily Baseline Mass</th>
              <th className="py-2.5 px-3">Criticality Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {depts.map((d) => (
              <tr key={d.code}>
                <td className="py-3 px-3 font-bold text-slate-200">{d.name}</td>
                <td className="py-3 px-3 text-cyan-400">{d.code}</td>
                <td className="py-3 px-3 text-emerald-400 font-bold">{d.baseline} kg/day</td>
                <td className="py-3 px-3 text-amber-400 font-bold">{d.criticality}/100</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
