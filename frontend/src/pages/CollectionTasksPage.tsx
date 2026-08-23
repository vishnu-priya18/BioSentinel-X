import React, { useEffect, useState } from 'react';
import { Truck, Calculator } from 'lucide-react';
import { ExplainScoreModal } from '../components/ExplainScoreModal';
import { apiService } from '../services/api';

export const CollectionTasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<any[]>([]);
  const [explainModalOpen, setExplainModalOpen] = useState<boolean>(false);
  const [activeTaskScore, setActiveTaskScore] = useState<number>(94.2);

  useEffect(() => {
    async function loadTasks() {
      try {
        const res = await fetch('/api/collection/tasks');
        if (res.ok) {
          setTasks(await res.json());
          return;
        }
      } catch (e) {
        console.warn("Using offline demo collection tasks");
      }
      setTasks([
        { task_id: 'task-1', passport_code: 'WP-DEMO-006-9012', department_name: 'ICU Ward', priority_score: 94.2, status: 'PENDING' },
        { task_id: 'task-2', passport_code: 'WP-DEMO-001-8819', department_name: 'Operation Theatre', priority_score: 88.0, status: 'ASSIGNED' },
        { task_id: 'task-3', passport_code: 'WP-DEMO-007-4120', department_name: 'Emergency Ward', priority_score: 72.5, status: 'EN_ROUTE' },
      ]);
    }
    loadTasks();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Truck className="w-5 h-5 text-cyan-400" />
            Risk-Aware Collection Task Prioritization
          </h2>
          <p className="text-xs text-slate-400">
            Collection routes optimized dynamically based on overflow risk, hazard risk, uncertainty, and department criticality.
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {tasks.map((task) => (
          <div key={task.task_id} className="glass-panel p-4 rounded-xl border border-slate-800 flex items-center justify-between font-mono text-xs">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center font-bold text-cyan-400 text-sm">
                {task.priority_score.toFixed(1)}
              </div>
              <div>
                <h4 className="font-bold text-slate-200">{task.department_name}</h4>
                <p className="text-[11px] text-slate-400 font-sans">Passport: {task.passport_code}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button 
                onClick={() => {
                  setActiveTaskScore(task.priority_score);
                  setExplainModalOpen(true);
                }}
                className="text-[11px] text-cyan-400 hover:text-cyan-300 font-sans bg-cyan-500/10 px-3 py-1.5 rounded-lg border border-cyan-500/20 flex items-center gap-1.5"
              >
                <Calculator className="w-3.5 h-3.5" />
                Explain Score
              </button>
              <span className="text-[10px] bg-slate-800 text-slate-300 px-2.5 py-1 rounded font-bold border border-slate-700">
                {task.status}
              </span>
            </div>
          </div>
        ))}
      </div>

      <ExplainScoreModal
        isOpen={explainModalOpen}
        onClose={() => setExplainModalOpen(false)}
        title="Collection Priority Math (P_task)"
        score={activeTaskScore}
        breakdown={{ overflow_risk: 96, hazard_risk: 91, uncertainty: 88, collection_delay: 84, department_criticality: 90, travel_cost: 76 }}
        weightedContributions={{ overflow_risk: 28.8, hazard_risk: 22.8, uncertainty: 13.2, collection_delay: 12.6, department_criticality: 9.0, travel_cost: 3.8 }}
        formulaExplanation="P_task = 0.30*Overflow + 0.25*Hazard + 0.15*Uncertainty + 0.15*Delay + 0.10*DeptCrit + 0.05*Travel"
      />
    </div>
  );
};
