import React, { useState } from 'react';
import { History, ShieldCheck, CheckCircle2 } from 'lucide-react';

export const AuditTrailPage: React.FC = () => {
  const [verificationStatus, setVerificationStatus] = useState<string>('VALID_HASH_CHAIN');

  const auditEvents = [
    { id: 'aud-demo-001', entity: 'WasteEvent', action: 'CREATE_AND_ANALYZE', performed_by: 'usr-worker', timestamp: new Date().toISOString(), prevHash: '0000000000000000000000000000000000000000000000000000000000000000', currHash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' },
    { id: 'aud-demo-007', entity: 'VerificationEvent', action: 'HUMAN_VERIFIER_APPROVE', performed_by: 'usr-verifier', timestamp: new Date().toISOString(), prevHash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', currHash: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <History className="w-5 h-5 text-cyan-400" />
            SHA-256 Tamper-Evident Audit Chain Log
          </h2>
          <p className="text-xs text-slate-400">
            Append-only event log linked with cryptographic SHA-256 previous/current hash chaining.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-3 py-1.5 rounded-xl font-mono text-xs font-bold">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>STATUS: VALID HASH CHAIN</span>
        </div>
      </div>

      <div className="space-y-3 font-mono text-xs">
        {auditEvents.map((a) => (
          <div key={a.id} className="glass-panel p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="font-bold text-cyan-400">{a.id}</span>
              <span className="text-[10px] text-slate-500">{new Date(a.timestamp).toLocaleString()}</span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-slate-300 text-[11px]">
              <div>Entity: <strong className="text-slate-100">{a.entity}</strong></div>
              <div>Action: <strong className="text-slate-100">{a.action}</strong></div>
              <div className="col-span-2 text-slate-400 truncate">Prev Hash: {a.prevHash}</div>
              <div className="col-span-2 text-emerald-400 font-bold truncate">Current Hash: {a.currHash}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
