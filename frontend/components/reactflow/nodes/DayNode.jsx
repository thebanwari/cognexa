/**
 * DayNode — Leaf node, compact AI learning step card.
 *
 * Typography:
 *   Title:  "Fundamentals"        ← cleaned (no "Day 1:" prefix)
 *   Label:  "Day 1"               ← from number
 *   Icon:   Lightbulb             ← learning step indicator
 */
import React, { useState } from 'react';
import { Handle, Position } from 'reactflow';

const DayNode = ({ id, data, selected }) => {
  const title = data?.title || id;
  const dayNumber = data?.number ?? '';
  const [hovered, setHovered] = useState(false);

  return (
    <>
      <Handle
        type="target"
        position={Position.Left}
        id={`${id}-in`}
        className="!w-2 !h-2 !bg-day-400 !border-[1.5px] !border-white !shadow-sm"
      />

      <div
        className={`
          group relative rounded-[11px] cursor-pointer select-none
          transition-all duration-[350ms] ease-out
          ${selected ? 'ring-[2px] ring-day-400/25' : ''}
        `}
        style={{
          width: 210,
          padding: '14px 16px',
          background: hovered
            ? 'linear-gradient(140deg, rgba(255,252,240,0.98) 0%, rgba(254,243,199,0.94) 100%)'
            : 'linear-gradient(140deg, rgba(255,252,240,0.92) 0%, rgba(254,243,199,0.84) 100%)',
          border: '1px solid rgba(245, 158, 11, 0.14)',
          boxShadow: hovered
            ? '0 10px 28px rgba(245,158,11,0.10), 0 0 0 1px rgba(245,158,11,0.06), inset 0 1px 0 rgba(255,255,255,0.8)'
            : '0 3px 12px rgba(245,158,11,0.05), inset 0 1px 0 rgba(255,255,255,0.6)',
          backdropFilter: 'blur(8px)',
          transform: hovered ? 'translateY(-1.5px)' : 'translateY(0)',
        }}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {/* Title row */}
        <div className="flex items-start gap-2.5 mb-2">
          {/* Lightbulb icon — learning step indicator */}
          <div
            className="flex items-center justify-center shrink-0 rounded-lg transition-all duration-300"
            style={{
              width: 24,
              height: 24,
              background: 'rgba(254,243,199,0.9)',
              transform: hovered ? 'scale(1.1)' : 'scale(1)',
            }}
          >
            <svg
              style={{ width: 13, height: 13 }}
              viewBox="0 0 24 24" fill="none" stroke="#b45309" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round"
            >
              <path d="M9 18h6M10 22h4M12 2a7 7 0 00-4 12.7V17a1 1 0 001 1h6a1 1 0 001-1v-2.3A7 7 0 0012 2z" />
            </svg>
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-[13px] font-bold text-gray-700 leading-snug line-clamp-2">
              {title}
            </p>
          </div>
        </div>

        {/* Day label row */}
        <div className="flex items-center gap-2 mt-1.5 pl-[34px]">
          <div
            className="flex items-center justify-center rounded-[5px] text-[8px] font-extrabold shrink-0"
            style={{
              width: 18,
              height: 18,
              background: 'rgba(254,243,199,0.95)',
              color: '#b45309',
            }}
          >
            {dayNumber}
          </div>
          <span className="text-[10px] font-medium text-amber-600/50">
            Day {dayNumber}
          </span>
        </div>
      </div>

      <Handle
        type="source"
        position={Position.Right}
        id={`${id}-out`}
        className="!opacity-0 !w-0 !h-0"
      />
    </>
  );
};

export default DayNode;