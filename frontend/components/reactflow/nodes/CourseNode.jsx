/**
 * CourseNode — Root/master node of the mindmap.
 * Premium design: larger, stronger visual emphasis, animated glow.
 *
 * Typography:
 *   Label:  "COURSE"
 *   Title:  "Introduction to Python"   ← prominent
 *   Stats:  "4 Weeks · 20 Days"        ← inline
 */
import React, { useState } from 'react';
import { Handle, Position } from 'reactflow';

const CourseNode = ({ id, data, selected }) => {
  const title = data?.title || 'Course';
  const weeks = data?.metadata?.weeks ?? '—';
  const days = data?.metadata?.totalDays ?? '—';
  const [hovered, setHovered] = useState(false);

  return (
    <>
      <Handle
        type="target"
        position={Position.Left}
        id={`${id}-in`}
        className="!opacity-0 !w-0 !h-0"
      />

      <div
        className={`
          group relative rounded-2xl cursor-pointer select-none
          transition-all duration-[400ms] ease-out
          ${selected ? 'ring-[3px] ring-course-500/25' : ''}
        `}
        style={{
          width: 360,
          padding: '22px 28px',
          background: hovered
            ? 'linear-gradient(145deg, rgba(238,242,255,0.98) 0%, rgba(224,231,255,0.96) 50%, rgba(237,233,254,0.94) 100%)'
            : 'linear-gradient(145deg, rgba(238,242,255,0.94) 0%, rgba(224,231,255,0.88) 50%, rgba(237,233,254,0.86) 100%)',
          border: '1px solid rgba(99, 102, 241, 0.15)',
          boxShadow: hovered
            ? '0 20px 56px rgba(99,102,241,0.18), 0 0 0 1px rgba(99,102,241,0.08), inset 0 1px 0 rgba(255,255,255,0.85)'
            : '0 8px 32px rgba(99,102,241,0.10), inset 0 1px 0 rgba(255,255,255,0.7)',
          backdropFilter: 'blur(16px)',
          transform: hovered ? 'translateY(-3px)' : 'translateY(0)',
        }}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {/* Animated glow ring */}
        <div
          className="absolute -inset-[2px] rounded-2xl pointer-events-none transition-opacity duration-500"
          style={{
            opacity: hovered ? 1 : 0,
            background: 'radial-gradient(ellipse at 50% 50%, rgba(99,102,241,0.08), transparent 70%)',
            filter: 'blur(20px)',
          }}
        />

        {/* Icon + Title */}
        <div className="relative flex items-start gap-4 mb-4">
          <div
            className="flex items-center justify-center w-11 h-11 rounded-xl shrink-0 transition-all duration-[400ms]"
            style={{
              background: 'linear-gradient(135deg, rgba(99,102,241,0.18), rgba(139,92,246,0.12))',
              transform: hovered ? 'scale(1.1) rotate(-2deg)' : 'scale(1) rotate(0)',
              boxShadow: hovered ? '0 4px 16px rgba(99,102,241,0.15)' : 'none',
            }}
          >
            <svg className="w-5.5 h-5.5 text-course-600" style={{ width: 22, height: 22 }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.7}
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-[9px] font-bold uppercase tracking-[0.15em] text-course-500/70 mb-1">
              Course
            </p>
            <h3 className="text-[16px] font-extrabold text-gray-800 leading-snug tracking-tight">
              {title}
            </h3>
          </div>
        </div>

        {/* Stats row */}
        <div className="relative flex items-center gap-2.5">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[10px] font-semibold bg-course-100/60 text-course-700/85 border border-course-200/30">
            <svg className="w-3 h-3 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {weeks} Weeks
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[10px] font-semibold bg-course-100/60 text-course-700/85 border border-course-200/30">
            <svg className="w-3 h-3 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {days} Days
          </span>
        </div>
      </div>

      <Handle
        type="source"
        position={Position.Right}
        id={`${id}-out`}
        className="!w-3.5 !h-3.5 !bg-course-400/80 !border-2 !border-white !shadow-md"
      />
    </>
  );
};

export default CourseNode;