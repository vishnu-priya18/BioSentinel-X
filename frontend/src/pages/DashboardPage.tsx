import React, { useEffect, useState } from 'react';
import { KpiCard } from '../components/KpiCard';
import { SafetyDisclaimerBanner } from '../components/SafetyDisclaimerBanner';
import { WhyNotPanel } from '../components/WhyNotPanel';
import { ExplainScoreModal } from '../components/ExplainScoreModal';
import { 
  Package, CheckCircle2, AlertTriangle, ShieldAlert, Truck, Activity, 
  ChevronRight, ArrowRight, Zap, Info, Calculator
} from 'lucide-react';
import { apiService } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [kpis, setKpis] = useState<any>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [explainModalOpen, setExplainModalOpen] = useState<boolean>(false);

  useEffect(() => {
    async function loadData() {
      const kpiRes = await apiService.getDashboardKpis();
      const evtRes = await apiService.getEvents();
      setKpis(kpiRes);
      setEvents(evtRes);
    }
    loadData();
  }, []);

  const wasteDistributionData = [
    { name: 'Yellow (Incineration)', value: 14, color: '#F59E0B' },
    { name: 'Red (Autoclave/Recycle)', value: 18, color: '#EF4444' },
    { name: 'White Sharps', value: 3, color: '#F8FAFC' },
    { name: 'Blue Glassware', value: 3, color: '#3B82F6' },
  ];

  const verificationData = [
    { name: 'Safe Auto-Approved', value: 28, fill: '#10B981' },
    { name: 'Human Verified', value: 5, fill: '#3B82F6' },
    { name: 'Abstained / Verify', value: 3, fill: '#F59E0B' },
    { name: 'High-Risk Escalated', value: 2, fill: '#EF4444' },
  ];

  return (
    <div className="space-y-6">
      <!-- Safety Disclaimer Banner -->
      <SafetyDisclaimerBanner />

      <!-- Top KPI Cards Grid -->
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <KpiCard title="Total Waste Today" value={kpis?.total_waste_events_today || 38} subtitle="Registered events" icon={Package} />
        <KpiCard title="Safe Auto-Approved" value={kpis?.verified_events || 28} subtitle="Low uncertainty" icon={CheckCircle2} />
        <KpiCard title="Pending Verification" value={kpis?.pending_verification || 7} subtitle="Abstained cases" icon={AlertTriangle} />
        <KpiCard title="High-Risk Events" value={kpis?.high_risk_events || 3} subtitle="Escalation active" icon={ShieldAlert} />
        <KpiCard title="Collection Tasks" value={kpis?.active_collection_tasks || 8} subtitle="Risk priority assigned" icon={Truck} />
        <KpiCard title="Stream Integrity" value={`${kpis?.waste_stream_integrity_score || 92.4}%`} subtitle="Department stability" icon={Activity} />
      </div>

      <!-- Main Command Grid -->
      <div className="grid grid-cols-12 gap-6">
        
        <!-- Left 8 Columns: Charts & Department Risk Heatmap -->
        <div className="col-span-12 lg:col-span-8 space-y-6">
          
          <!-- Charts Row -->
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <!-- Waste Distribution Chart -->
            <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
              <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300">
                Waste Category Distribution
              </h3>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={wasteDistributionData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70} label>
                      {wasteDistributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            <!-- Verification Breakdown Chart -->
            <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
              <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300">
                Decision Policy Outcome Breakdown
              </h3>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={verificationData}>
                    <XAxis dataKey="name" stroke="#64748B" fontSize={10} tickLine={false} />
                    <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                    <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }} />
                    <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                      {verificationData.map((entry, index) => (
                        <Cell key={`bar-${index}`} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

          </div>

          <!-- Department Risk Heatmap -->
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300">
                Department Waste Integrity & Collection Risk Heatmap
              </h3>
              <button 
                onClick={() => setExplainModalOpen(true)}
                className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1.5 bg-cyan-500/10 px-3 py-1.5 rounded-lg border border-cyan-500/20"
              >
                <Calculator className="w-3.5 h-3.5" />
                Explain Score Math
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-slate-200">
                  <span>ICU Ward (ICU-01)</span>
                  <span className="text-emerald-400 font-mono">94.2 STABLE</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-emerald-400 h-full" style={{ width: '94%' }}></div>
                </div>
                <p className="text-[11px] text-slate-400">Baseline: 12.5kg • Pending: 2 tasks</p>
              </div>

              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-slate-200">
                  <span>Emergency Ward (EMG-01)</span>
                  <span className="text-blue-400 font-mono">88.0 WATCH</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-blue-400 h-full" style={{ width: '88%' }}></div>
                </div>
                <p className="text-[11px] text-slate-400">Baseline: 15.0kg • Pending: 1 task</p>
              </div>

              <div className="bg-slate-900 p-4 rounded-xl border border-rose-500/40 bg-rose-950/20 space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-rose-300">
                  <span>Pathology Lab (LAB-01)</span>
                  <span className="text-rose-400 font-mono font-bold">48.5 CRITICAL</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className="bg-rose-500 h-full" style={{ width: '48%' }}></div>
                </div>
                <p className="text-[11px] text-rose-300/80">Weight Anomaly Z = +4.8 (18.5kg vs 2.1kg)</p>
              </div>
            </div>
          </div>

          <!-- Recent Events Table -->
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300">
                Recent Biomedical Waste Events & Decision Traces
              </h3>
              <button onClick={() => navigate('/evidence')} className="text-xs text-cyan-400 hover:underline">
                View All Events →
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 text-[10px] uppercase tracking-wider">
                    <th className="py-2.5 px-3">Event Code</th>
                    <th className="py-2.5 px-3">Department</th>
                    <th className="py-2.5 px-3">Category</th>
                    <th className="py-2.5 px-3">Mass Weight</th>
                    <th className="py-2.5 px-3">Opacity</th>
                    <th className="py-2.5 px-3">Decision State</th>
                    <th className="py-2.5 px-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {events.map((e) => (
                    <tr key={e.id} className="hover:bg-slate-900/60 transition">
                      <td className="py-3 px-3 font-bold text-cyan-400">{e.event_code}</td>
                      <td className="py-3 px-3 text-slate-200">{e.dept_name}</td>
                      <td className="py-3 px-3 text-slate-300">{e.declared_category}</td>
                      <td className="py-3 px-3 text-emerald-400 font-bold">{e.weight_kg} kg</td>
                      <td className="py-3 px-3">
                        <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${
                          e.opacity_state === 'NOT_OBSERVABLE' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400'
                        }`}>
                          {e.opacity_state}
                        </span>
                      </td>
                      <td className="py-3 px-3">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                          e.decision_state === 'SAFE_TO_AUTOMATE' ? 'bg-emerald-500/10 text-emerald-400' :
                          e.decision_state === 'NEEDS_VERIFICATION' ? 'bg-amber-500/10 text-amber-400' : 'bg-rose-500/10 text-rose-400'
                        }`}>
                          {e.decision_state}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right">
                        <button 
                          onClick={() => navigate(`/evidence`)}
                          className="text-[11px] text-cyan-400 hover:text-cyan-300 font-bold font-sans"
                        >
                          View Trace →
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- Right 4 Columns: "Why Not?" Featured Panel & Alerts Feed -->
        <div className="col-span-12 lg:col-span-4 space-y-6">
          
          <!-- Sample Why Not Panel for DEMO-004 -->
          <WhyNotPanel 
            predictedCategory="Red"
            confidence={0.88}
            decisionState="HIGH_RISK_ESCALATION"
            reasons={[
              { status: 'PASS', source: 'Image Quality', message: 'Clear visual image score (0.82)', technical_value: '0.82', explanation: 'Sufficient clarity' },
              { status: 'PASS', source: 'AI Confidence', message: 'Model confidence 88%', technical_value: '0.88', explanation: 'High raw classification confidence' },
              { status: 'FAIL', source: 'Barcode Cross-Check', message: 'Scanned Yellow barcode on Red bag', technical_value: 'CONFLICT', explanation: 'CPCB string mismatch detected' },
              { status: 'FAIL', source: 'Weight Anomaly', message: 'Weight deviates from baseline (Z = +4.8)', technical_value: 'Z=+4.8', explanation: 'Unexpected mass surge' }
            ]}
          />

          <!-- Recent Alerts Feed -->
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300 flex items-center justify-between">
              <span>Active System Alerts</span>
              <span className="text-[10px] font-mono bg-rose-500/10 text-rose-400 px-2 py-0.5 rounded border border-rose-500/20">2 Critical</span>
            </h3>

            <div className="space-y-3 text-xs">
              <div className="bg-rose-950/40 border border-rose-500/40 p-3.5 rounded-xl space-y-1">
                <div className="flex items-center justify-between text-rose-300 font-bold">
                  <span>Pathology Lab Weight Anomaly</span>
                  <span className="text-[10px] font-mono bg-rose-500/20 px-1.5 py-0.5 rounded">Z = +4.8</span>
                </div>
                <p className="text-slate-300">Lab waste bag DEMO-005 registered 18.5kg vs 2.1kg baseline (8.8x multiplier).</p>
              </div>

              <div className="bg-amber-950/40 border border-amber-500/40 p-3.5 rounded-xl space-y-1">
                <div className="flex items-center justify-between text-amber-300 font-bold">
                  <span>Barcode Category Mismatch</span>
                  <span className="text-[10px] font-mono bg-amber-500/20 px-1.5 py-0.5 rounded">DEMO-004</span>
                </div>
                <p className="text-slate-300">Yellow CPCB barcode attached to Red recyclable plastic tubing.</p>
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- Explain Score Modal -->
      <ExplainScoreModal
        isOpen={explainModalOpen}
        onClose={() => setExplainModalOpen(false)}
        title="Collection Priority Score (P_task)"
        score={94.2}
        breakdown={{
          overflow_risk: 96,
          hazard_risk: 91,
          uncertainty: 88,
          collection_delay: 84,
          department_criticality: 90,
          travel_cost: 76
        }}
        weightedContributions={{
          overflow_risk: 28.8,
          hazard_risk: 22.8,
          uncertainty: 13.2,
          collection_delay: 12.6,
          department_criticality: 9.0,
          travel_cost: 3.8
        }}
        formulaExplanation="Priority Score = 0.30*Overflow + 0.25*Hazard + 0.15*Uncertainty + 0.15*Delay + 0.10*DeptCrit + 0.05*Travel"
      />
    </div>
  );
};
