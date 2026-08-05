/**
 * FlashcardControls — Navigation, progress dots, progress bar.
 * Sits below the card in the modal.
 */
import React from 'react';

const FlashcardControls = ({
  current,
  total,
  onPrevious,
  onNext,
  onFlip,
  onRegenerate,
  isRegenerating,
}) => {
  return (
    <div className="w-full max-w-lg mx-auto mt-6 space-y-4">
      {/* Navigation row */}
      <div className="flex items-center justify-between gap-3">
        {/* Previous */}
        <button
          onClick={onPrevious}
          disabled={total <= 1}
          className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-[12px] font-semibold
                     bg-white/80 text-gray-600 border border-gray-200/50
                     hover:bg-gray-50 hover:border-gray-300/50
                     transition-all duration-200
                     disabled:opacity-40 disabled:cursor-not-allowed"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Prev
        </button>

        {/* Progress dots */}
        <div className="flex items-center gap-1.5">
          {Array.from({ length: total }, (_, i) => (
            <div
              key={i}
              className="rounded-full transition-all duration-300"
              style={{
                width: i === current ? 18 : 6,
                height: 6,
                background: i === current
                  ? 'linear-gradient(90deg, #818cf8, #6366f1)'
                  : 'rgba(203,213,225,0.5)',
                borderRadius: 3,
              }}
            />
          ))}
        </div>

        {/* Next */}
        <button
          onClick={onNext}
          disabled={total <= 1}
          className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-[12px] font-semibold
                     bg-white/80 text-gray-600 border border-gray-200/50
                     hover:bg-gray-50 hover:border-gray-300/50
                     transition-all duration-200
                     disabled:opacity-40 disabled:cursor-not-allowed"
        >
          Next
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Progress bar */}
      <div className="w-full h-1 rounded-full bg-gray-200/40 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-400 ease-out"
          style={{
            width: `${((current + 1) / total) * 100}%`,
            background: 'linear-gradient(90deg, #a5b4fc, #6366f1)',
          }}
        />
      </div>

      {/* Action buttons */}
      <div className="flex items-center justify-center gap-3">
        <button
          onClick={onFlip}
          className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-[11px] font-semibold
                     bg-course-50/80 text-course-600 border border-course-200/40
                     hover:bg-course-100/80 transition-all duration-200"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Flip Card
        </button>

        <button
          onClick={onRegenerate}
          disabled={isRegenerating}
          className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-[11px] font-semibold
                     bg-gray-50/80 text-gray-500 border border-gray-200/40
                     hover:bg-gray-100/80 transition-all duration-200
                     disabled:opacity-50"
        >
          <svg
            className={`w-3.5 h-3.5 ${isRegenerating ? 'animate-spin' : ''}`}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {isRegenerating ? 'Generating…' : 'Regenerate'}
        </button>
      </div>

      {/* Keyboard hints */}
      <p className="text-center text-[10px] text-gray-400">
        ← Prev · → Next · Space Flip · Esc Close
      </p>
    </div>
  );
};

export default FlashcardControls;
