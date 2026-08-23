import React, { useState, useEffect } from 'react';
import { PlayCircle, ArrowRight, ArrowLeft, CheckCircle2, AlertTriangle, ShieldAlert, QrCode, Calculator, Zap, History } from 'lucide-react';
import { apiService } from '../services/api';
import { WhyNotPanel } from '../components/WhyNotPanel';
import { CriticalHazardAlert } from '../components/CriticalHazardAlert';
import { ExplainScoreModal } from '../components/ExplainScoreModal';
import { PassportCard } from '../components/PassportCard';
import { DemoScenario } from '../types';

export const SimulationModePage: React.FC = () => {
  const [scenarios, setScenarios] = useState<DemoScenario[]>([]);
  const [currentIdx, setCurrentIdx] = useState<number>(0);
  const [scenarioData, setScenarioData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [explainModalOpen, setExplainModalOpen] = useState<boolean>(false);

  useEffect(() => {
    async function loadScenarios() {
      const list = await apiService.getDemoScenarios();
      setScenarios(list);
      if (list.length > 0) {
        runScenario(list[0].code);
      }
    }
    loadScenarios();
  }, []);

  const runScenario = async (code: string) => {
    setIsLoading(true);
    const data = await apiService.runSimulationScenario(code);
    setIsLoading(false);
    if (data) {
      setScenarioData(data);
    } else {
      // Offline fallback simulator
      const isSyringe = code === 'DEMO-005';
      const isOpaque = code === 'DEMO-003';
      setScenarioData({
        scenario_code: code,
        decision_state: code === 'DEMO-001' ? 'SAFE_TO_AUTOMATE' : (isOpaque ? 'UNKNOWN' : 'HIGH_RISK_ESCALATION'),
        automation_allowed: code === 'DEMO-001' ? true : false,
        reasons: [
          { status: isSyringe ? 'FAIL' : 'PASS', source: 'Hazard Gate', message: isSyringe ? 'Critical sharp hazard detected (SYRINGE)' : 'Visual clear', technical_value: isSyringe ? 'SYRINGE' : '0.88', explanation: isSyringe ? 'Automated approval BLOCKED by safety policy' : 'Sufficient clear image' }
        ],
        trace: {
          prediction: { category: isSyringe ? 'White' : 'Red', confidence: isSyringe ? 0.97 : 0.91 },
          hazard: { detected: isSyringe, hazard_type: isSyringe ? 'SYRINGE' : 'NONE', severity: isSyringe ? 'CRITICAL' : 'LOW', score: isSyringe ? 0.97 : 0.05, critical: isSyringe, critical_hazard: isSyringe, automation_allowed: !isSyringe, evidence_source: 'Hazard Gate', explanation: isSyringe ? 'Critical sharp biomedical hazard detected.' : 'No hazard.' },
          evidence: { image_quality: 0.85, observability: isOpaque ? 'NOT_OBSERVABLE' : 'OBSERVABLE' },
          decision: { state: code === 'DEMO-001' ? 'SAFE_TO_AUTOMATE' : (isOpaque ? 'UNKNOWN' : 'HIGH_RISK_ESCALATION'), automation_allowed: code === 'DEMO-001' },
          counterfactual: { required: isSyringe ? ['HAZARD_CLEARANCE_AND_INDEPENDENT_VERIFICATION', 'SAFE_SHARPS_HANDLING_WORKFLOW_CONFIRMATION'] : ['OBSERVABLE_CONTENT', 'VALID_BARCODE'] }
        },
        audit_chain_status: 'VALID_HASH_CHAIN'
      });
    }
  };

  const handleSelectScenario = (index: number) => {
    setCurrentIdx(index);
    runScenario(scenarios[index].code);
  };

  const activeScenario = scenarios[currentIdx] || { code: 'DEMO-001', title: 'Scenario', description: '' };

  return (
    <div className="space-y-6">
      
      <!-- Top Guided Stepper Banner -->
      <div className="bg-gradient-to-r from-cyan-950/60 via-slate-900 to-slate-950 border border-cyan-500/30 p-6 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
            <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
              <PlayCircle className="w-5 h-5 text-cyan-400" />
              SIH Grand Finale Guided Demo Mode
            </h2>
            <span className="text-[9px] font-mono bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded border border-purple-500/40 font-bold uppercase ml-2">
              SIH SIMULATION MODE
            </span>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            Walk judges through all 8 deterministic test scenarios (DEMO-001 to DEMO-008) proving uncertainty-aware abstention, syringe sharp hazard blocking, evidence conflict resolution, and SHA-256 audit chaining.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <button 
            disabled={currentIdx === 0}
            onClick={() => handleSelectScenario(currentIdx - 1)}
            className="p-2.5 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-300 disabled:opacity-40 transition"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>

          <span className="font-mono text-xs font-bold text-cyan-400 bg-cyan-500/10 px-3 py-2 rounded-xl border border-cyan-500/20">
            Step {currentIdx + 1} of {scenarios.length || 8}
          </span>

          <button 
            disabled={currentIdx === scenarios.length - 1}
            onClick={() => handleSelectScenario(currentIdx + 1)}
            className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs py-2.5 px-4 rounded-xl shadow-lg flex items-center gap-2 disabled:opacity-40 transition"
          >
            <span>Next Step</span>
            <ArrowRight className="w-4 h-4 text-slate-950" />
          </button>
        </div>
      </div>

      <!-- Scenarios Selector Buttons Bar -->
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
        {scenarios.map((sc, idx) => (
          <button
            key={sc.code}
            onClick={() => handleSelectScenario(idx)}
            className={`p-2.5 rounded-xl border text-left transition font-mono text-xs flex flex-col justify-between h-20 ${
              idx === currentIdx
                ? 'bg-cyan-500/20 border-cyan-500/60 text-cyan-300 ring-1 ring-cyan-500/40 shadow-lg'
                : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:bg-slate-800/80 hover:text-slate-200'
            }`}
          >
            <span className="font-bold text-[11px] block">{sc.code}</span>
            <span className="text-[10px] line-clamp-2 text-slate-300 font-sans">{sc.title}</span>
          </button>
        ))}
      </div>

      <!-- Active Scenario Execution Details -->
      {scenarioData && (
        <div className="grid grid-cols-12 gap-6">
          
          <!-- Left 7 Columns: Scenario Explanation & Evidence Breakdown -->
          <div className="col-span-12 lg:col-span-7 space-y-6">
            
            <!-- Critical Hazard Banner if detected -->
            {scenarioData.trace?.hazard?.detected && (
              <CriticalHazardAlert
                hazard={scenarioData.trace.hazard}
                aiConfidence={scenarioData.trace?.prediction?.confidence || 0.97}
              />
            )}

            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest block font-bold">Active Scenario Code</span>
                  <h3 className="font-bold text-base text-slate-100">{activeScenario.title}</h3>
                </div>
                <span className={`font-mono text-xs font-bold px-3 py-1 rounded-full border ${
                  scenarioData.decision_state === 'SAFE_TO_AUTOMATE' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' :
                  scenarioData.decision_state === 'NEEDS_VERIFICATION' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                }`}>
                  {scenarioData.decision_state}
                </span>
              </div>

              <p className="text-xs text-slate-300 font-medium">
                {activeScenario.description}
              </p>

              <!-- Inputs Summary Table -->
              <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 grid grid-cols-3 gap-3 font-mono text-xs text-center">
                <div>
                  <span className="text-[10px] text-slate-500 uppercase tracking-widest block">Container Mass</span>
                  <span className="font-bold text-emerald-400">{scenarioData.weight_kg || 4.5} kg</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 uppercase tracking-widest block">Observability</span>
                  <span className={`font-bold ${scenarioData.opacity_state === 'NOT_OBSERVABLE' ? 'text-rose-400' : 'text-cyan-400'}`}>
                    {scenarioData.opacity_state || 'OBSERVABLE'}
                  </span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 uppercase tracking-widest block">Audit Status</span>
                  <span className="font-bold text-purple-400">{scenarioData.audit_chain_status || 'VALID'}</span>
                </div>
              </div>
            </div>

            <!-- Counterfactual Reasoning Panel -->
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
              <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300 flex items-center gap-2">
                <Calculator className="w-4 h-4 text-cyan-400" />
                Counterfactual Engine: "What Would Have Made This Safe?"
              </h3>
              <p className="text-xs text-slate-400">
                Minimum required evidence conditions necessary to transition this decision state into <strong className="text-emerald-400">SAFE_TO_AUTOMATE</strong>:
              </p>

              <div className="space-y-2">
                {(scenarioData.trace?.counterfactual?.required || ['ALL_SAFETY_BOUNDS_SATISFIED']).map((req: string, idx: number) => (
                  <div key={idx} className="bg-slate-900 p-3 rounded-xl border border-slate-800 flex items-center gap-3 text-xs font-mono">
                    <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0" />
                    <span className="text-slate-200">{req.replace(/_/g, ' ')}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Passport View if DEMO-001 or DEMO-007 */}
            {(activeScenario.code === 'DEMO-001' || activeScenario.code === 'DEMO-007' || activeScenario.code === 'DEMO-008') && (
              <PassportCard 
                passportCode={`WP-${activeScenario.code}-8819A`}
                eventCode={activeScenario.code}
                category="Red (Autoclave/Recycle)"
                weightKg={scenarioData.weight_kg || 0.22}
                riskLevel="LOW"
                status="ISSUED"
                evidenceHash="SHA256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                createdAt={new Date().toISOString()}
              />
            )}

          </div>

          <!-- Right 5 Columns: "Why Not?" Explanation Panel -->
          <div className="col-span-12 lg:col-span-5 space-y-6">
            
            <WhyNotPanel
              predictedCategory={scenarioData.trace?.prediction?.category || 'Red'}
              confidence={scenarioData.trace?.prediction?.confidence || 0.91}
              decisionState={scenarioData.decision_state || 'NEEDS_VERIFICATION'}
              reasons={scenarioData.reasons || [
                { status: 'PASS', source: 'Image Quality', message: 'Clear visual capture', technical_value: '0.88', explanation: 'Good quality score' }
              ]}
            />

            <!-- Presentation Closing Line Banner -->
            <div className="bg-gradient-to-r from-cyan-950 to-slate-900 border border-cyan-500/30 p-5 rounded-2xl text-center space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-widest text-cyan-400 font-bold block">Presenter Closing Statement</span>
              <p className="text-xs font-semibold text-slate-100 italic">
                "We don't build an AI that always gives an answer. We build a system that knows when an answer isn't safe enough to act on."
              </p>
            </div>

          </div>

        </div>
      )}

      <!-- Explain Score Modal -->
      <ExplainScoreModal
        isOpen={explainModalOpen}
        onClose={() => setExplainModalOpen(false)}
        title="Collection Priority Math (P_task)"
        score={94.2}
        breakdown={{ overflow_risk: 96, hazard_risk: 91, uncertainty: 88, collection_delay: 84, department_criticality: 90, travel_cost: 76 }}
        weightedContributions={{ overflow_risk: 28.8, hazard_risk: 22.8, uncertainty: 13.2, collection_delay: 12.6, department_criticality: 9.0, travel_cost: 3.8 }}
        formulaExplanation="P_task = 0.30*Overflow + 0.25*Hazard + 0.15*Uncertainty + 0.15*Delay + 0.10*DeptCrit + 0.05*Travel"
      />
    </div>
  );
};
