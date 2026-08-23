import React from 'react';
import { BarChart3 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

export const AnalyticsPage: React.FC = () => {
  const trendData = [
    { day: 'Mon', Yellow: 12, Red: 15, White: 2 },
    { day: 'Tue', Yellow: 14, Red: 18, White: 3 },
    { day: 'Wed', Yellow: 10, Red: 14, White: 4 },
    { day: 'Thu', Yellow: 16, Red: 19, White: 2 },
    { day: 'Fri', Yellow: 15, Red: 22, White: 5 },
    { day: 'Sat', Yellow: 11, Red: 16, White: 1 },
    { day: 'Sun', Yellow: 14, Red: 18, White: 3 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-cyan-400" />
            Hospital Analytics & Operational Trends
          </h2>
          <p className="text-xs text-slate-400">
            Historical waste volume generation, category breakdown, and anomaly frequency over time.
          </p>
        </div>
      </div>

      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300">
          7-Day Waste Generation Volume Trend (kg)
        </h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={trendData}>
              <XAxis dataKey="day" stroke="#64748B" />
              <YAxis stroke="#64748B" />
              <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155' }} />
              <Bar dataKey="Yellow" fill="#F59E0B" stackId="a" />
              <Bar dataKey="Red" fill="#EF4444" stackId="a" />
              <Bar dataKey="White" fill="#38BDF8" stackId="a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
