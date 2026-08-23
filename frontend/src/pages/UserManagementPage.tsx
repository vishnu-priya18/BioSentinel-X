import React from 'react';
import { Users } from 'lucide-react';

export const UserManagementPage: React.FC = () => {
  const users = [
    { name: 'Dr. Rajesh Sharma', email: 'admin@sentinel.org', role: 'ADMIN', dept: 'ICU Ward' },
    { name: 'Anita Roy', email: 'supervisor@sentinel.org', role: 'SUPERVISOR', dept: 'Emergency' },
    { name: 'Staff Worker #412', email: 'worker@sentinel.org', role: 'SANITATION_WORKER', dept: 'ICU Ward' },
    { name: 'Safety Verifier Vikram', email: 'verifier@sentinel.org', role: 'VERIFIER', dept: 'Pathology Lab' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Users className="w-5 h-5 text-cyan-400" />
            User Administration & Role RBAC
          </h2>
          <p className="text-xs text-slate-400">
            Role-Based Access Control (Admin, Supervisor, Sanitation Worker, Verifier, Viewer).
          </p>
        </div>
      </div>

      <div className="glass-panel p-5 rounded-2xl border border-slate-800">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400">
              <th className="py-2.5 px-3">Name</th>
              <th className="py-2.5 px-3">Email</th>
              <th className="py-2.5 px-3">Role</th>
              <th className="py-2.5 px-3">Department</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {users.map((u) => (
              <tr key={u.email}>
                <td className="py-3 px-3 font-bold text-slate-200">{u.name}</td>
                <td className="py-3 px-3 text-slate-400">{u.email}</td>
                <td className="py-3 px-3 font-bold text-cyan-400">{u.role}</td>
                <td className="py-3 px-3 text-slate-300">{u.dept}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
