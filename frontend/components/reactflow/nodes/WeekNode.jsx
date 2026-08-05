/**
 * WeekNode — Second-level with rotating color palette.
 *
 * Clean typography hierarchy (NO duplication):
 *   Title:    "Core Concepts"      ← cleaned (prefix stripped by parser)
 *   Subtitle: "Week 1 · 5 days"   ← single line
 *   Toggle:   ▶ chevron
 */
import React, { useCallback, useState } from 'react';
import { Handle, Position } from 'reactflow';

const WEEK_COLORS = [
  { bg: 'rgba(236,253,245,0.93)', border: 'rgba(16,185,129,0.16)', accent: '#059669', badge: 'rgba(209,250,229,0.85)', text: '#065f46', glow: 'rgba(16,185,129,0.10)', light: 'rgba(16,185,129,0.06)' },
  { bg: 'rgba(239,246,255,0.93)', border: 'rgba(59,130,246,0.16)',  accent: '#2563eb', badge: 'rgba(219,234,254,0.85)', text: '#1e40af', glow: 'rgba(59,130,246,0.10)', light: 'rgba(59,130,246,0.06)' },
  { bg: 'rgba(254,242,242,0.93)', border: 'rgba(239,68,68,0.16)',   accent: '#dc2626', badge: 'rgba(254,226,226,0.85)', text: '#991b1b', glow: 'rgba(239,68,68,0.10)', light: 'rgba(239,68,68,0.06)' },
  { bg: 'rgba(254,249,195,0.93)', border: 'rgba(202,138,4,0.16)',   accent: '#ca8a04', badge: 'rgba(254,249,195,0.85)', text: '#854d0e', glow: 'rgba(202,138,4,0.10)', light: 'rgba(202,138,4,0.06)' },
  { bg: 'rgba(243,232,255,0.93)', border: 'rgba(139,92,246,0.16)',  accent: '#7c3aed', badge: 'rgba(237,233,254,0.85)', text: '#5b21b6', glow: 'rgba(139,92,246,0.10)', light: 'rgba(139,92,246,0.06)' },
  { bg: 'rgba(255,241,242,0.93)', border: 'rgba(244,63,94,0.16)',   accent: '#e11d48', badge: 'rgba(255,228,230,0.85)', text: '#9f1239', glow: 'rgba(244,63,94,0.10)', light: 'rgba(244,63,94,0.06)' },
];

const WeekNode = ({ id, data, selected }) => {
  const title = data?.title || id;
  const weekNum = data?.metadata?.weekNumber ?? data?.number ?? '';
  const daysCount = data?.metadata?.days ?? 0;
  const isCollapsed = data?.isCollapsed ?? true;
  const onToggle = data?.onToggle;
  const [hovered, setHovered] = useState(false);

  const palette = WEEK_COLORS[(weekNum - 1) % WEEK_COLORS.length] || WEEK_COLORS[0];

  const handleToggle = useCallback((e) => {
    e.stopPropagation();
    if (typeof onToggle === 'function') onToggle(id);
  }, [id, onToggle]);

  return (
    <>
      <Handle
        type="target"
        position={Position.Left}
        id={`${id}-in`}
        className="!w-2.5 !h-2.5 !border-2 !border-white !shadow-sm"
        style={{ background: palette.accent }}
      />

      <div
        className={`
          group relative rounded-xl cursor-pointer select-none
          transition-all duration-[350ms] ease-out
          ${selected ? 'ring-[2px]' : ''}
        `}
        style={{
          width: 230,
          padding: '14px 16px',
          background: palette.bg,
          border: `1px solid ${palette.border}`,
          boxShadow: hovered
            ? `0 12px 36px ${palette.glow}, 0 0 0 1px ${palette.border}, inset 0 1px 0 rgba(255,255,255,0.8)`
            : `0 4px 16px ${palette.light}, inset 0 1px 0 rgba(255,255,255,0.65)`,
          backdropFilter: 'blur(10px)',
          transform: hovered ? 'translateY(-2px)' : 'translateY(0)',
          ...(selected ? { ringColor: `${palette.accent}30` } : {}),
        }}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {/* Title — largest element, NO prefix duplication */}
        <p
          className="text-[14px] font-bold leading-snug mb-2 line-clamp-2"
          style={{ color: palette.text }}
        >
          {title}
        </p>

        {/* Subtitle row: Week N · X days [toggle] */}
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5 min-w-0">
            {/* Colored pill with week number */}
            <div
              className="flex items-center justify-center shrink-0 rounded-md text-[9px] font-extrabold transition-transform duration-300"
              style={{
                width: 22,
                height: 20,
                background: palette.badge,
                color: palette.accent,
                transform: hovered ? 'scale(1.1)' : 'scale(1)',
              }}
            >
              {weekNum}
            </div>
            <span className="text-[11px] font-medium" style={{ color: palette.text, opacity: 0.6 }}>
              Week {weekNum}
            </span>
            <span className="text-[11px]" style={{ color: palette.text, opacity: 0.25 }}>·</span>
            <span className="text-[11px] font-semibold" style={{ color: palette.accent, opacity: 0.7 }}>
              {daysCount} {daysCount === 1 ? 'day' : 'days'}
            </span>
          </div>

          {/* Toggle button */}
          <button
            onClick={handleToggle}
            aria-label={isCollapsed ? 'Expand' : 'Collapse'}
            className="flex items-center justify-center shrink-0 rounded-md transition-all duration-200 hover:scale-110 active:scale-95"
            style={{
              width: 24,
              height: 24,
              background: isCollapsed ? palette.badge : `${palette.accent}15`,
              color: palette.accent,
            }}
          >
            <svg
              className={`transition-transform duration-300 ${isCollapsed ? '' : 'rotate-90'}`}
              style={{ width: 12, height: 12 }}
              viewBox="0 0 24 24" fill="none" stroke="currentColor"
              strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"
            >
              <path d="M9 18l6-6-6-6" />
            </svg>
          </button>
        </div>
      </div>

      <Handle
        type="source"
        position={Position.Right}
        id={`${id}-out`}
        className="!w-2.5 !h-2.5 !border-2 !border-white !shadow-sm"
        style={{ background: palette.accent }}
      />
    </>
  );
};

export default WeekNode;