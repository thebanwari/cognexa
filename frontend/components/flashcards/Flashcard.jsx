/**
 * Flashcard — Single card with CSS 3D flip animation.
 *
 * Front: question + difficulty badge
 * Back:  answer + hint + tags
 *
 * Uses CSS perspective + rotateY for premium flip.
 * All styling uses inline + Tailwind to match design system.
 */
import React from 'react';

const DIFFICULTY_COLORS = {
  easy:   { bg: 'rgba(209,250,229,0.8)', text: '#065f46', label: 'Easy' },
  medium: { bg: 'rgba(254,243,199,0.8)', text: '#854d0e', label: 'Medium' },
  hard:   { bg: 'rgba(254,226,226,0.8)', text: '#991b1b', label: 'Hard' },
};

const Flashcard = ({ card, isFlipped, onFlip, index, total }) => {
  if (!card) return null;

  const diff = DIFFICULTY_COLORS[card.difficulty] || DIFFICULTY_COLORS.easy;

  return (
    <div
      className="w-full max-w-lg mx-auto cursor-pointer select-none"
      style={{ perspective: 1200 }}
      onClick={onFlip}
    >
      <div
        className="relative w-full transition-transform duration-500 ease-out"
        style={{
          height: 320,
          transformStyle: 'preserve-3d',
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0)',
        }}
      >
        {/* ── FRONT ────────────────────────────────────────────── */}
        <div
          className="absolute inset-0 rounded-2xl p-7 flex flex-col"
          style={{
            backfaceVisibility: 'hidden',
            background: 'linear-gradient(145deg, rgba(238,242,255,0.96), rgba(224,231,255,0.92))',
            border: '1px solid rgba(99,102,241,0.12)',
            boxShadow: '0 8px 32px rgba(99,102,241,0.08), inset 0 1px 0 rgba(255,255,255,0.8)',
            backdropFilter: 'blur(12px)',
          }}
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-5">
            <span
              className="px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider"
              style={{ background: diff.bg, color: diff.text }}
            >
              {diff.label}
            </span>
            <span className="text-[11px] font-medium text-gray-400">
              {index + 1} / {total}
            </span>
          </div>

          {/* Question */}
          <div className="flex-1 flex items-center justify-center px-2">
            <p className="text-[17px] font-semibold text-gray-800 text-center leading-relaxed">
              {card.question}
            </p>
          </div>

          {/* Hint */}
          <p className="text-[11px] text-center text-gray-400 mt-4">
            Tap to reveal answer
          </p>
        </div>

        {/* ── BACK ─────────────────────────────────────────────── */}
        <div
          className="absolute inset-0 rounded-2xl p-7 flex flex-col"
          style={{
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)',
            background: 'linear-gradient(145deg, rgba(236,253,245,0.96), rgba(209,250,229,0.92))',
            border: '1px solid rgba(16,185,129,0.12)',
            boxShadow: '0 8px 32px rgba(16,185,129,0.08), inset 0 1px 0 rgba(255,255,255,0.8)',
            backdropFilter: 'blur(12px)',
          }}
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <span className="px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider bg-emerald-100/80 text-emerald-700">
              Answer
            </span>
            <span className="text-[11px] font-medium text-gray-400">
              {index + 1} / {total}
            </span>
          </div>

          {/* Answer */}
          <div className="flex-1 flex flex-col justify-center px-1">
            <p className="text-[15px] font-medium text-gray-700 text-center leading-relaxed mb-4">
              {card.answer}
            </p>

            {/* Hint */}
            {card.hint && (
              <div className="flex items-start gap-2 px-3 py-2.5 rounded-xl bg-white/50 border border-emerald-100/40">
                <svg className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-[11px] text-emerald-700/70 leading-snug">{card.hint}</p>
              </div>
            )}
          </div>

          {/* Tags */}
          {card.tags && card.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-3">
              {card.tags.map((tag, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded-md text-[9px] font-semibold bg-emerald-50/60 text-emerald-600/70 border border-emerald-100/30"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Flashcard;
