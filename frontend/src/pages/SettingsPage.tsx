import React, { useEffect, useState } from 'react';
import { Settings } from 'lucide-react';
import { apiService } from '../services/api';

export const SettingsPage: React.FC = () => {
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    async function loadSettings() {
      try {
        const res = await fetch('/api/settings');
        if (res.ok) setConfig(await res.json());
      } catch (e) {
        console.warn("Using default settings");
      }
    }
    loadSettings();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Settings className="w-5 h-5 text-cyan-400" />
            System & Decision Engine Threshold Settings
          </h2>
          <p className="text-xs text-slate-400">
            Configurable uncertainty entropy limits, conflict score thresholds, and calibration metadata.
          </p>
        </div>
      </div>

      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 font-mono text-xs">
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex justify-between">
          <span className="text-slate-400">HIGH CONFLICT THRESHOLD:</span>
          <span className="text-cyan-400 font-bold">0.60</span>
        </div>
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex justify-between">
          <span className="text-slate-400">HIGH RISK THRESHOLD:</span>
          <span className="text-cyan-400 font-bold">0.65</span>
        </div>
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex justify-between">
          <span className="text-slate-400">HIGH UNCERTAINTY THRESHOLD:</span>
          <span className="text-cyan-400 font-bold">0.60</span>
        </div>
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex justify-between">
          <span className="text-slate-400">VERIFICATION THRESHOLD:</span>
          <span className="text-amber-400 font-bold">0.35</span>
        </div>
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 flex justify-between">
          <span className="text-slate-400">IMAGE QUALITY MINIMUM THRESHOLD:</span>
          <span className="text-emerald-400 font-bold">0.40</span>
        </div>
      </div>
    </div>
  );
};
