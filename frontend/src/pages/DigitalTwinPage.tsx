import React, { useEffect, useState } from 'react';
import { Building2, Activity, ShieldAlert } from 'lucide-react';

export const DigitalTwinPage: React.FC = () => {
  const [twinData, setTwinData] = useState<any[]>([]);

  useEffect(() => {
    async function loadTwin() {
      try {
        const res = await fetch('/api/digital-twin');
        if (res.ok) {
          setTwinData(await res.json());
          return;
        }
      } catch (e) {
        console.warn("Using offline digital twin data");
      }
      setTwinData([
        { dept_id: '1', name: 'ICU Ward', code: 'ICU-01', baseline_daily_waste_kg: 12.5, current_volume_kg: 9.8, integrity: { integrity_score: 94.2, status: 'STABLE', color_hex: '#10B981' } },
        { dept_id: '2', name: 'Emergency Ward', code: 'EMG-01', baseline_daily_waste_kg: 15.0, current_volume_kg: 11.2, integrity: { integrity_score: 88.0, status: 'WATCH', color_hex: '#3B82F6' } },
        { dept_id: '3', name: 'Pathology Lab', code: 'LAB-01', baseline_daily_waste_kg: 2.1, current_volume_kg: 18.5, integrity: { integrity_score: 48.5, status: 'CRITICAL', color_hex: '#EF4444' } },
      ]);
    }
    loadTwin();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Building2 className="w-5 h-5 text-cyan-400" />
            Hospital Spatial Digital Twin
          </h2>
          <p className="text-xs text-slate-400">
            Real-time ward waste volume, risk heatmaps, and department integrity scores.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {twinData.map((d) => (
          <div key={d.code} className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-sm text-slate-200">{d.name}</h3>
              <span 
                className="text-[10px] font-mono font-bold px-2 py-0.5 rounded border"
                style={{ color: d.integrity?.color_hex, borderColor: d.integrity?.color_hex + '40', backgroundColor: d.integrity?.color_hex + '10' }}
              >
                {d.integrity?.status}
              </span>
            </div>

            <div className="space-y-2 font-mono text-xs">
              <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
                <span className="text-slate-500">Integrity Score:</span>
                <span className="font-bold" style={{ color: d.integrity?.color_hex }}>{d.integrity?.integrity_score}%</span>
              </div>

              <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex justify-between">
                <span className="text-slate-500">Accumulated Mass:</span>
                <span className="text-emerald-400 font-bold">{d.current_volume_kg} kg</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
