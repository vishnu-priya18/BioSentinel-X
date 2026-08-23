import React, { useState } from 'react';
import { Camera, QrCode, ArrowRight, ShieldAlert, CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';
import { apiService } from '../services/api';
import { WasteCategoryBadge } from '../components/WasteCategoryBadge';
import { CriticalHazardAlert } from '../components/CriticalHazardAlert';

export const ScanWastePage: React.FC = () => {
  const [step, setStep] = useState<number>(1);
  const [barcode, setBarcode] = useState<string>('CPCB-IND-2026-90821-WHT');
  const [declaredCategory, setDeclaredCategory] = useState<string>('White');
  const [weightKg, setWeightKg] = useState<number>(0.25);
  const [opacityState, setOpacityState] = useState<string>('OBSERVABLE');
  const [userNotes, setUserNotes] = useState<string>('Syringe / Needle');
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [decisionResult, setDecisionResult] = useState<any>(null);

  const handleRunAnalysis = async () => {
    setIsAnalyzing(true);
    setStep(4);

    try {
      const res = await apiService.analyzeEvent({
        event_code: `EVT-${Date.now()}`,
        dept_id: 'dept-icu',
        declared_category_code: declaredCategory,
        weight_kg: weightKg,
        container_type: 'PLASTIC_BAG',
        opacity_state: opacityState,
        user_notes: userNotes,
        barcode_scanned: barcode
      });

      setTimeout(() => {
        setIsAnalyzing(false);
        if (res) {
          setDecisionResult(res);
        } else {
          // Fallback simulation
          const isSyringe = userNotes.toLowerCase().includes('syringe') || userNotes.toLowerCase().includes('needle');
          const isOpaque = opacityState === 'NOT_OBSERVABLE';
          setDecisionResult({
            decision_state: isOpaque ? 'UNKNOWN' : (isSyringe ? 'HIGH_RISK_ESCALATION' : 'SAFE_TO_AUTOMATE'),
            automation_allowed: isOpaque || isSyringe ? false : true,
            trace: {
              prediction: { object_class: isSyringe ? 'SYRINGE' : 'IV_TUBE', category: isSyringe ? 'WHITE' : 'RED', confidence: 0.97 },
              classification: { object_class: isSyringe ? 'SYRINGE' : 'IV_TUBE', waste_type: isSyringe ? 'SHARPS' : 'CONTAMINATED_PLASTIC', bag_category: isSyringe ? 'WHITE' : 'RED' },
              hazard: { detected: isSyringe, hazard_type: isSyringe ? 'SYRINGE' : 'NONE', severity: isSyringe ? 'CRITICAL' : 'LOW', score: isSyringe ? 0.97 : 0.05, critical: isSyringe, critical_hazard: isSyringe, automation_allowed: !isSyringe, explanation: isSyringe ? 'Critical sharp biomedical hazard detected.' : 'No hazard.' },
              decision: { state: isOpaque ? 'UNKNOWN' : (isSyringe ? 'HIGH_RISK_ESCALATION' : 'SAFE_TO_AUTOMATE'), automation_allowed: !isSyringe }
            }
          });
        }
        setStep(5);
      }, 1200);
    } catch (e) {
      setIsAnalyzing(false);
      setStep(5);
    }
  };

  const resetForm = () => {
    setStep(1);
    setDecisionResult(null);
    setUserNotes('Syringe / Needle');
  };

  const trace = decisionResult?.trace || {};

  return (
    <div className="max-w-xl mx-auto p-4 flex flex-col gap-6">
      
      <!-- Top Mobile Header -->
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex items-center justify-between shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Camera className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-bold text-base text-slate-100">Sanitation Worker Mobile PWA</h2>
            <p className="text-xs text-slate-400">Biomedical Waste Evidence Collection Workflow</p>
          </div>
        </div>
        <span className="text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2.5 py-1 rounded-full font-bold">
          Step {step} of 5
        </span>
      </div>

      <!-- Step 1: Scan Barcode / QR -->
      {step === 1 && (
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5 animate-fadeIn">
          <div className="text-center space-y-1">
            <h3 className="font-bold text-base text-slate-100">Step 1: Scan CPCB Barcode or QR Code</h3>
            <p className="text-xs text-slate-400">Point device camera at mandatory container sticker</p>
          </div>

          <div className="bg-slate-900 rounded-xl border border-slate-800 p-8 text-center space-y-3 relative overflow-hidden">
            <div className="w-16 h-16 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 mx-auto flex items-center justify-center">
              <QrCode className="w-8 h-8" />
            </div>
            <p className="text-xs text-slate-300 font-mono">Simulated Camera Viewport Scanner Active</p>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 max-w-xs mx-auto">
              <label className="text-[10px] text-slate-500 uppercase tracking-widest block text-left">Scanned String</label>
              <input 
                type="text" 
                value={barcode}
                onChange={(e) => setBarcode(e.target.value)}
                className="bg-transparent font-mono text-xs font-bold text-cyan-400 w-full focus:outline-none mt-1"
              />
            </div>
          </div>

          <button
            onClick={() => setStep(2)}
            className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs py-3 rounded-xl shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2 transition"
          >
            <span>Continue to Photo Capture</span>
            <ArrowRight className="w-4 h-4 text-slate-950" />
          </button>
        </div>
      )}

      <!-- Step 2: Photo Capture -->
      {step === 2 && (
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5 animate-fadeIn">
          <div className="text-center space-y-1">
            <h3 className="font-bold text-base text-slate-100">Step 2: Capture Visual Evidence</h3>
            <p className="text-xs text-slate-400">Take clear photo of bag and container material</p>
          </div>

          <div className="bg-slate-900 rounded-xl border border-slate-800 p-8 text-center space-y-3">
            <div className="w-16 h-16 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 mx-auto flex items-center justify-center">
              <Camera className="w-8 h-8" />
            </div>
            <p className="text-xs text-slate-300 font-medium">Camera Snapshot Loaded</p>

            <div className="flex justify-center gap-3">
              <span className="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 px-2.5 py-1 rounded border border-emerald-500/20">
                Quality: 0.91 (Good)
              </span>
              <span className="text-[10px] font-mono bg-cyan-500/10 text-cyan-400 px-2.5 py-1 rounded border border-cyan-500/20">
                Resolution: 1920x1080
              </span>
            </div>
          </div>

          <div className="flex gap-3">
            <button onClick={() => setStep(1)} className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs py-3 rounded-xl border border-slate-700">
              Back
            </button>
            <button onClick={() => setStep(3)} className="flex-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs py-3 px-4 rounded-xl shadow-lg flex items-center justify-center gap-2">
              <span>Next: Enter Weight & Item Type</span>
              <ArrowRight className="w-4 h-4 text-slate-950" />
            </button>
          </div>
        </div>
      )}

      <!-- Step 3: Enter Metadata & Notes -->
      {step === 3 && (
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5 animate-fadeIn">
          <div className="text-center space-y-1">
            <h3 className="font-bold text-base text-slate-100">Step 3: Enter Scale Weight & Item Details</h3>
            <p className="text-xs text-slate-400">Specify physical item description and container metadata</p>
          </div>

          <div className="space-y-4 text-xs font-mono">
            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 space-y-1.5">
              <label className="text-[10px] text-slate-400 uppercase tracking-widest block font-sans">Item Description (e.g. Syringe, Needle, IV Tube, Gauze)</label>
              <input 
                type="text" 
                placeholder="e.g. Syringe or Needle"
                value={userNotes}
                onChange={(e) => setUserNotes(e.target.value)}
                className="w-full bg-slate-950 text-amber-300 font-bold p-2.5 rounded-lg border border-slate-800 focus:outline-none"
              />
            </div>

            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 space-y-1.5">
              <label className="text-[10px] text-slate-400 uppercase tracking-widest block font-sans">Declared Container Label</label>
              <select 
                value={declaredCategory} 
                onChange={(e) => setDeclaredCategory(e.target.value)}
                className="w-full bg-slate-950 text-slate-200 p-2.5 rounded-lg border border-slate-800 focus:outline-none"
              >
                <option value="White">White (Sharps)</option>
                <option value="Red">Red (Contaminated Plastic)</option>
                <option value="Yellow">Yellow (Soiled / Anatomical Incineration)</option>
                <option value="Blue">Blue (Glassware / Ampoules)</option>
              </select>
            </div>

            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 space-y-1.5">
              <label className="text-[10px] text-slate-400 uppercase tracking-widest block font-sans">Scale Weight (kg)</label>
              <input 
                type="number" 
                step="0.05"
                value={weightKg}
                onChange={(e) => setWeightKg(parseFloat(e.target.value) || 0)}
                className="w-full bg-slate-950 text-slate-200 p-2.5 rounded-lg border border-slate-800 font-bold focus:outline-none"
              />
            </div>

            <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 space-y-1.5">
              <label className="text-[10px] text-slate-400 uppercase tracking-widest block font-sans">Container Opacity State</label>
              <select 
                value={opacityState} 
                onChange={(e) => setOpacityState(e.target.value)}
                className="w-full bg-slate-950 text-cyan-400 font-bold p-2.5 rounded-lg border border-slate-800 focus:outline-none"
              >
                <option value="OBSERVABLE">OBSERVABLE (Clear Container)</option>
                <option value="PARTIALLY_OBSERVABLE">PARTIALLY OBSERVABLE (Semi-Translucent)</option>
                <option value="NOT_OBSERVABLE">NOT OBSERVABLE (Opaque / Sealed Bag)</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleRunAnalysis}
            className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs py-3.5 rounded-xl shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2 transition"
          >
            <span>EXECUTE OBJECT CLASSIFICATION & POLICY ANALYSIS</span>
            <ArrowRight className="w-4 h-4 text-slate-950" />
          </button>
        </div>
      )}

      <!-- Step 4: Analyzing -->
      {step === 4 && (
        <div className="glass-panel p-10 rounded-2xl border border-slate-800 text-center space-y-4 animate-fadeIn">
          <div className="w-16 h-16 rounded-full bg-cyan-500/20 border border-cyan-500/40 text-cyan-400 mx-auto flex items-center justify-center animate-spin">
            <RefreshCw className="w-8 h-8" />
          </div>
          <h3 className="font-bold text-base text-slate-100">Analyzing Object & Safety Gate...</h3>
          <p className="text-xs text-slate-400 font-mono">Object Detection → Waste Category Mapper → Hazard Gate → Deterministic Policy Engine</p>
        </div>
      )}

      <!-- Step 5: Worker Decision Result View -->
      {step === 5 && decisionResult && (
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5 animate-fadeIn">
          
          {/* Section A: AI Object Prediction */}
          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-mono block font-sans">A. AI Object Detection</span>
            <div className="flex items-center justify-between font-mono">
              <span className="text-cyan-400 font-bold text-base">
                💉 {trace.classification?.object_class || trace.prediction?.object_class || 'UNKNOWN'}
              </span>
              <span className="text-slate-300 text-xs font-bold">
                Confidence: {((trace.prediction?.confidence || 0.97) * 100).toFixed(1)}%
              </span>
            </div>
          </div>

          {/* Section B: Waste Disposal Category */}
          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-2">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-mono block font-sans">B. Waste Disposal Category</span>
            <div className="flex items-center justify-between font-mono">
              <span className="text-slate-200 font-bold text-xs">
                Type: {trace.classification?.waste_type || 'SHARPS'}
              </span>
              <WasteCategoryBadge 
                category={trace.classification?.bag_category || trace.prediction?.category || 'WHITE'} 
                size="md"
              />
            </div>
          </div>

          {/* Section C: Safety Decision */}
          <div className="text-center space-y-2">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-mono font-sans block">C. Safety & Operational Decision</span>

            {decisionResult.decision_state === 'SAFE_TO_AUTOMATE' && (
              <div className="p-4 rounded-xl border border-emerald-500/40 bg-emerald-500/10 text-emerald-400 text-center space-y-1">
                <CheckCircle2 className="w-8 h-8 mx-auto text-emerald-400" />
                <h3 className="font-mono text-xl font-bold">🟢 SAFE TO AUTOMATE</h3>
                <p className="text-xs text-emerald-300/80 font-sans">Waste collection pickup approved. Waste Passport issued.</p>
              </div>
            )}

            {decisionResult.decision_state === 'NEEDS_VERIFICATION' && (
              <div className="p-4 rounded-xl border border-amber-500/40 bg-amber-500/10 text-amber-400 text-center space-y-1">
                <AlertTriangle className="w-8 h-8 mx-auto text-amber-400" />
                <h3 className="font-mono text-xl font-bold">🟡 VERIFICATION REQUIRED</h3>
                <p className="text-xs text-amber-300/80 font-sans">Moderate evidence uncertainty. Routed to human verifier queue.</p>
              </div>
            )}

            {decisionResult.decision_state === 'UNKNOWN' && (
              <div className="p-4 rounded-xl border border-purple-500/40 bg-purple-500/10 text-purple-300 text-center space-y-1">
                <ShieldAlert className="w-8 h-8 mx-auto text-purple-400" />
                <h3 className="font-mono text-xl font-bold">⚪ CONTENT NOT OBSERVABLE</h3>
                <p className="text-xs text-purple-200/80 font-sans">Opaque bag prohibits visual classification. Refuses to guess hidden contents.</p>
              </div>
            )}

            {decisionResult.decision_state === 'HIGH_RISK_ESCALATION' && (
              <div className="p-4 rounded-xl border-2 border-rose-500 bg-rose-950/40 text-rose-200 text-center space-y-1 shadow-xl">
                <ShieldAlert className="w-8 h-8 mx-auto text-rose-400 animate-pulse" />
                <h3 className="font-mono text-xl font-bold text-rose-100">🔴 HIGH-RISK ESCALATION</h3>
                <p className="text-xs text-rose-300 font-sans font-bold">AUTOMATION: BLOCKED</p>
                <p className="text-[11px] text-slate-300 font-sans">Critical sharp hazard detected. Requires puncture-proof sharp container handling.</p>
              </div>
            )}
          </div>

          <button
            onClick={resetForm}
            className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs py-3 rounded-xl border border-slate-700 transition"
          >
            Scan Another Waste Container
          </button>
        </div>
      )}

    </div>
  );
};
