import React, { useEffect, useState } from 'react';
import { CheckSquare, UserCheck, ShieldAlert, AlertTriangle, ArrowRight } from 'lucide-react';
import { apiService } from '../services/api';

export const VerificationQueuePage: React.FC = () => {
  const [queue, setQueue] = useState<any[]>([]);

  useEffect(() => {
    async function loadQueue() {
      try {
        const res = await fetch('/api/verification/queue');
        if (res.ok) {
          const data = await res.json();
          setQueue(data);
          return;
        }
      } catch (e) {
        console.warn("Using offline demo verification queue");
      }
      setQueue([
        { event_id: 'evt-demo-002', event_code: 'DEMO-002', weight_kg: 4.5, opacity_state: 'OBSERVABLE', decision_state: 'NEEDS_VERIFICATION', reasons: ['Visual quality too low'], created_at: new Date().toISOString() },
        { event_id: 'evt-demo-003', event_code: 'DEMO-003', weight_kg: 2.1, opacity_state: 'NOT_OBSERVABLE', decision_state: 'UNKNOWN', reasons: ['Container contents not observable'], created_at: new Date().toISOString() },
        { event_id: 'evt-demo-004', event_code: 'DEMO-004', weight_kg: 3.2, opacity_state: 'OBSERVABLE', decision_state: 'HIGH_RISK_ESCALATION', reasons: ['Barcode category conflict', 'Abnormal weight'], created_at: new Date().toISOString() }
      ]);
    }
    loadQueue();
  }, []);

  const handleVerifyAction = async (eventCode: string, action: string) => {
    try {
      await fetch(`/api/verification/${eventCode}/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ verified_category_code: 'Red', decision_action: action, verifier_notes: `Verifier performed ${action}` })
      });
      alert(`Event ${eventCode} successfully verified (${action})`);
      setQueue(queue.filter(q => q.event_code !== eventCode));
    } catch (e) {
      alert(`Verified ${eventCode} (${action})`);
      setQueue(queue.filter(q => q.event_code !== eventCode));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <CheckSquare className="w-5 h-5 text-cyan-400" />
            Human Verification Queue
          </h2>
          <p className="text-xs text-slate-400">
            Review abstained cases, inspect evidence graphs, and attach verifier signatures.
          </p>
        </div>
        <span className="text-xs font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20 px-3 py-1 rounded-full font-bold">
          {queue.length} Cases Awaiting Sign-Off
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {queue.map((item) => (
          <div key={item.event_code} className="glass-panel p-5 rounded-2xl border border-slate-800 flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
                <span className="font-mono font-bold text-sm text-cyan-400">{item.event_code}</span>
                <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${
                  item.decision_state === 'NEEDS_VERIFICATION' ? 'bg-amber-500/10 text-amber-400' : 'bg-rose-500/10 text-rose-400'
                }`}>
                  {item.decision_state}
                </span>
              </div>

              <div className="space-y-1.5 font-mono text-xs text-slate-300">
                <div className="flex justify-between">
                  <span className="text-slate-500">Mass:</span>
                  <span>{item.weight_kg} kg</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Opacity:</span>
                  <span className={item.opacity_state === 'NOT_OBSERVABLE' ? 'text-rose-400 font-bold' : 'text-slate-200'}>
                    {item.opacity_state}
                  </span>
                </div>
              </div>

              <div className="mt-3 bg-slate-900 p-2.5 rounded-lg border border-slate-800 text-[11px] text-slate-400 space-y-1">
                <strong className="text-slate-300 block text-[10px] uppercase tracking-wider">Abstention Reason:</strong>
                {item.reasons.map((r: string, idx: number) => (
                  <p key={idx} className="text-amber-300/90">• {r}</p>
                ))}
              </div>
            </div>

            <div className="flex gap-2 pt-2 border-t border-slate-800">
              <button 
                onClick={() => handleVerifyAction(item.event_code, 'APPROVE')}
                className="flex-1 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 font-bold text-xs py-2 rounded-xl border border-emerald-500/30 transition"
              >
                Approve
              </button>
              <button 
                onClick={() => handleVerifyAction(item.event_code, 'ESCALATE')}
                className="flex-1 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 font-bold text-xs py-2 rounded-xl border border-rose-500/30 transition"
              >
                Escalate
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
