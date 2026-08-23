import React from 'react';

interface WasteCategoryBadgeProps {
  category: string;
  wasteType?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const WasteCategoryBadge: React.FC<WasteCategoryBadgeProps> = ({
  category,
  wasteType,
  size = 'md'
}) => {
  const catUpper = (category || 'UNKNOWN').toUpperCase();

  const getStyle = (cat: string) => {
    switch (cat) {
      case 'WHITE':
        return 'bg-slate-100 border-2 border-slate-400 text-slate-950 font-extrabold shadow-sm';
      case 'RED':
        return 'bg-rose-600 border border-rose-400 text-white font-extrabold shadow-sm';
      case 'YELLOW':
        return 'bg-amber-400 border border-amber-500 text-slate-950 font-extrabold shadow-sm';
      case 'BLUE':
        return 'bg-blue-600 border border-blue-400 text-white font-extrabold shadow-sm';
      default:
        return 'bg-purple-900/60 border border-purple-500/40 text-purple-200 font-extrabold';
    }
  };

  const getSizeStyle = (s: 'sm' | 'md' | 'lg') => {
    switch (s) {
      case 'sm':
        return 'px-2 py-0.5 text-[10px]';
      case 'lg':
        return 'px-4 py-2 text-sm font-mono tracking-wider';
      default:
        return 'px-3 py-1 text-xs font-mono';
    }
  };

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-lg ${getStyle(catUpper)} ${getSizeStyle(size)}`}>
      <span>{catUpper}</span>
      {wasteType && (
        <span className="opacity-80 font-normal text-[10px] uppercase font-sans">
          ({wasteType.replace(/_/g, ' ')})
        </span>
      )}
    </span>
  );
};
