import React from 'react';
import { PassportCard } from '../components/PassportCard';
import { QrCode } from 'lucide-react';

export const WastePassportPage: React.FC = () => {
  const passports = [
    { passportCode: 'WP-DEMO-001-9081A', eventCode: 'DEMO-001', category: 'Red (Autoclave/Recycle)', weightKg: 0.22, riskLevel: 'LOW', status: 'ISSUED', evidenceHash: 'SHA256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', createdAt: new Date().toISOString() },
    { passportCode: 'WP-DEMO-007-4120B', eventCode: 'DEMO-007', category: 'Yellow (Incineration)', weightKg: 4.5, riskLevel: 'LOW', status: 'ISSUED', evidenceHash: 'SHA256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', createdAt: new Date().toISOString() },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <QrCode className="w-5 h-5 text-cyan-400" />
            Waste Passport & Dynamic QR Registry
          </h2>
          <p className="text-xs text-slate-400">
            Digital custody passport issued for verified biomedical waste events.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {passports.map((p) => (
          <PassportCard key={p.passportCode} {...p} />
        ))}
      </div>
    </div>
  );
};
