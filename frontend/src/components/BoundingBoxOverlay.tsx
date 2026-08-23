import React from 'react';

export interface BoundingBoxData {
  object_id?: string;
  class_name: string;
  display_name?: string;
  confidence: number;
  bounding_box: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
  hazard_type?: string;
  hazard_severity?: string;
}

interface BoundingBoxOverlayProps {
  imageSrc?: string | null;
  objects?: BoundingBoxData[];
  containerWidth?: number;
  containerHeight?: number;
}

export const BoundingBoxOverlay: React.FC<BoundingBoxOverlayProps> = ({
  imageSrc,
  objects = [],
  containerWidth = 600,
  containerHeight = 400
}) => {
  const getBoxColor = (severity?: string) => {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL':
        return { border: 'border-rose-500', bg: 'bg-rose-500/20', text: 'bg-rose-600 text-white' };
      case 'HIGH':
        return { border: 'border-amber-500', bg: 'bg-amber-500/20', text: 'bg-amber-500 text-slate-950 font-bold' };
      case 'MEDIUM':
        return { border: 'border-blue-500', bg: 'bg-blue-500/20', text: 'bg-blue-600 text-white' };
      default:
        return { border: 'border-emerald-500', bg: 'bg-emerald-500/20', text: 'bg-emerald-500 text-slate-950 font-bold' };
    }
  };

  return (
    <div className="relative w-full overflow-hidden rounded-xl border border-slate-800 bg-slate-950 shadow-xl">
      {imageSrc ? (
        <img 
          src={imageSrc} 
          alt="Detection Target" 
          className="w-full h-auto max-h-[450px] object-contain mx-auto block" 
        />
      ) : (
        <div className="w-full h-64 bg-slate-900/80 flex flex-col items-center justify-center text-slate-500 font-mono text-xs gap-2">
          <span>Camera Viewport & Bounding Box Overlay Ready</span>
          <span className="text-[10px] text-slate-600">Simulated 1920x1080 Viewport Coordinate Canvas</span>
        </div>
      )}

      <!-- Overlay Bounding Boxes -->
      <div className="absolute inset-0 pointer-events-none">
        {objects.map((obj, idx) => {
          const colors = getBoxColor(obj.hazard_severity);
          // Scale 1920x1080 normalized coordinates to percentages
          const leftPct = (obj.bounding_box.x1 / 1920) * 100;
          const topPct = (obj.bounding_box.y1 / 1080) * 100;
          const widthPct = ((obj.bounding_box.x2 - obj.bounding_box.x1) / 1920) * 100;
          const heightPct = ((obj.bounding_box.y2 - obj.bounding_box.y1) / 1080) * 100;

          return (
            <div
              key={obj.object_id || idx}
              style={{
                left: `${Math.max(5, Math.min(80, leftPct))}%`,
                top: `${Math.max(5, Math.min(75, topPct))}%`,
                width: `${Math.max(25, Math.min(65, widthPct))}%`,
                height: `${Math.max(25, Math.min(65, heightPct))}%`
              }}
              className={`absolute border-2 ${colors.border} ${colors.bg} rounded-lg transition-all animate-fadeIn flex flex-col justify-between p-1.5 shadow-lg`}
            >
              <div className="self-start">
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-extrabold uppercase shadow ${colors.text}`}>
                  {obj.display_name || obj.class_name} {(obj.confidence * 100).toFixed(1)}%
                </span>
              </div>

              {obj.hazard_severity === 'CRITICAL' && (
                <div className="self-end bg-rose-950/90 text-rose-300 border border-rose-500/50 px-2 py-0.5 rounded text-[9px] font-mono font-bold">
                  ⚠ CRITICAL SHARP
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
