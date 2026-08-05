/**
 * Sidebar — Compact node detail panel (slides in from right).
 * Narrower 260px width, tighter spacing.
 */
import React from 'react';

const TYPE_CONFIG = {
  course: {
    label: 'Course',
    icon: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>
    ),
    badgeClass: 'bg-course-100/80 text-course-700',
    dot: '#818cf8',
  },
  week: {
    label: 'Week',
    icon: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    ),
    badgeClass: 'bg-week-100/80 text-week-700',
    dot: '#34d399',
  },
  day: {
    label: 'Day',
    icon: (
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
      </svg>
    ),
    badgeClass: 'bg-day-100/80 text-day-700',
    dot: '#fbbf24',
  },
};

const Sidebar = ({ selectedNodeDetails, onClose, onGenerateFlashcards }) => {
  if (!selectedNodeDetails) return null;

  const { id, title, type, description, metadata } = selectedNodeDetails;
  const config = TYPE_CONFIG[type] || TYPE_CONFIG.course;

  return (
    <div
      className="h-full overflow-y-auto border-l"
      style={{
        width: 260,
        background: 'rgba(255,255,255,0.92)',
        backdropFilter: 'blur(16px)',
        borderColor: 'rgba(226,232,240,0.5)',
        boxShadow: '-4px 0 24px rgba(0,0,0,0.04)',
      }}
    >
      <div className="px-4 py-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-[0.12em]">
            Details
          </p>
          <button
            onClick={onClose}
            className="p-1 rounded-md hover:bg-gray-100/80 transition-colors"
          >
            <svg className="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Type badge */}
        <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[10px] font-semibold mb-3 ${config.badgeClass}`}>
          {config.icon}
          {config.label}
        </span>

        {/* Title */}
        <div className="mb-4">
          <p className="text-[9px] font-semibold text-gray-400 uppercase tracking-wider mb-0.5">Title</p>
          <h4 className="text-[15px] font-bold text-gray-900 leading-snug">{title}</h4>
        </div>

        {/* Node ID */}
        <div className="mb-4">
          <p className="text-[9px] font-semibold text-gray-400 uppercase tracking-wider mb-0.5">ID</p>
          <p className="text-[11px] font-mono bg-gray-50/80 px-2.5 py-1.5 rounded-lg text-gray-500 border border-gray-100/80 truncate">
            {id}
          </p>
        </div>

        {/* Description */}
        {description && (
          <div className="mb-4">
            <p className="text-[9px] font-semibold text-gray-400 uppercase tracking-wider mb-0.5">Description</p>
            <p className="text-[12px] text-gray-600 leading-relaxed">{description}</p>
          </div>
        )}

        {/* Metadata */}
        {metadata && Object.keys(metadata).length > 0 && (
          <div className="mb-4">
            <p className="text-[9px] font-semibold text-gray-400 uppercase tracking-wider mb-1.5">Metadata</p>
            <div className="space-y-1.5">
              {Object.entries(metadata).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between py-1.5 px-2.5 bg-gray-50/70 rounded-lg border border-gray-100/60">
                  <span className="text-[10px] font-medium text-gray-400 capitalize">
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </span>
                  <span className="text-[10px] font-bold text-gray-700">{String(value)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── AI Actions (day nodes only) ────────────────────── */}
        {type === 'day' && onGenerateFlashcards && (
          <div className="mb-4 pt-3 border-t border-gray-100/60">
            <p className="text-[9px] font-semibold text-gray-400 uppercase tracking-wider mb-2">AI Tools</p>
            <button
              onClick={() => onGenerateFlashcards(title)}
              className="w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-[11px] font-semibold
                         bg-gradient-to-r from-course-500 to-course-600
                         text-white shadow-sm
                         hover:from-course-600 hover:to-course-700
                         active:scale-[0.98]
                         transition-all duration-200"
            >
              <svg className="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707" />
              </svg>
              Generate Flashcards
            </button>
          </div>
        )}

        {/* Hierarchy breadcrumb */}
        <div className="pt-3 border-t border-gray-100/60">
          <p className="text-[9px] font-semibold text-gray-400 uppercase tracking-wider mb-2">Hierarchy</p>
          <div className="flex items-center gap-1.5 text-[10px] text-gray-400">
            {['course', 'week', 'day'].map((t, i) => (
              <React.Fragment key={t}>
                {i > 0 && <span className="text-gray-300">→</span>}
                <span className="flex items-center gap-1">
                  <span
                    className="w-2 h-2 rounded-full transition-transform duration-200"
                    style={{
                      background: TYPE_CONFIG[t]?.dot || '#94a3b8',
                      transform: type === t ? 'scale(1.3)' : 'scale(1)',
                      boxShadow: type === t ? `0 0 6px ${TYPE_CONFIG[t]?.dot}40` : 'none',
                    }}
                  />
                  <span className={type === t ? 'text-gray-700 font-semibold' : ''}>
                    {t.charAt(0).toUpperCase() + t.slice(1)}
                  </span>
                </span>
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;