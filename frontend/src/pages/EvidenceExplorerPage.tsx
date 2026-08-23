import React, { useState } from 'react';
import { Compass, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';

export const EvidenceExplorerPage: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<string>('decision');

  const nodes = [
    { id: 'event', label: 'Waste Event: DEMO-004', type: 'Event', source: 'Staff Scanner', detail: 'Event code DEMO-004 registered at Pathology Lab' },
    { id: 'barcode', label: 'Barcode: CPCB-YEL-9082', type: 'Evidence', source: 'OpenCV OCR', detail: 'Yellow category barcode string scanned on Red bag' },
    { id: 'image', label: 'Image Quality: 0.82 (Good)', type: 'Evidence', source: 'Camera Evaluator', detail: 'Laplacian variance 142.5 - Clear focus' },
    { id: 'weight', label: 'Scale Weight: 3.2 kg', type: 'Evidence', source: 'IMU Filtered Scale', detail: 'Lab baseline is 2.1kg (Abnormal weight warning)' },
    { id: 'ai', label: 'AI Prediction: RED (88%)', type: 'AI Classifier', source: 'Demo MobileNetV4', detail: 'Visual feature vector matches Red recyclable plastic' },
    { id: 'uncertainty', label: 'Softmax Entropy H = 0.58', type: 'Uncertainty', source: 'Entropy Estimator', detail: 'Medium-high uncertainty due to conflict' },
    { id: 'decision', label: 'Decision: HIGH_RISK_ESCALATION', type: 'Policy Engine', source: 'Deterministic Rules', detail: 'Barcode conflict + Abnormal weight triggers escalation' },
  ];

  const activeDetail = nodes.find(n => n.id === selectedNode) || nodes[0];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="font-bold text-lg text-slate-100 flex items-center gap-2">
            <Compass className="w-5 h-5 text-cyan-400" />
            Interactive Evidence Graph Explorer
          </h2>
          <p className="text-xs text-slate-400">
            Click any node in the evidence flow to inspect exact source data, reliability scores, and reasoning.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        <!-- Visual Node Graph Container -->
        <div className="col-span-12 lg:col-span-8 glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300">
            Evidence Graph Flow View (DEMO-004)
          </h3>

          <div className="bg-slate-900/90 rounded-xl border border-slate-800 p-6 space-y-3 font-mono text-xs">
            {nodes.map((node) => (
              <div 
                key={node.id}
                onClick={() => setSelectedNode(node.id)}
                className={`p-3.5 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                  selectedNode === node.id 
                    ? 'bg-cyan-500/20 border-cyan-500/60 text-cyan-300 ring-1 ring-cyan-500/40 shadow-lg'
                    : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
                  <span className="font-bold">{node.label}</span>
                </div>
                <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded border border-slate-700">{node.type}</span>
              </div>
            ))}
          </div>
        </div>

        <!-- Right Detail Panel -->
        <div className="col-span-12 lg:col-span-4 glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="font-semibold text-sm uppercase tracking-wider text-slate-300">
            Node Technical Inspection
          </h3>

          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-3 font-mono text-xs">
            <div>
              <span className="text-[10px] text-slate-500 uppercase tracking-widest block">Node Identifier</span>
              <span className="font-bold text-cyan-400">{activeDetail.id}</span>
            </div>

            <div>
              <span className="text-[10px] text-slate-500 uppercase tracking-widest block">Source Engine</span>
              <span className="text-slate-200 font-bold">{activeDetail.source}</span>
            </div>

            <div>
              <span className="text-[10px] text-slate-500 uppercase tracking-widest block">Technical Explanation</span>
              <p className="text-slate-300 font-sans mt-1 leading-relaxed">{activeDetail.detail}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
