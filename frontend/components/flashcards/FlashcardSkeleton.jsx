/**
 * FlashcardSkeleton — Shimmer loading card.
 * Shown while flashcards are being generated.
 */
import React from 'react';

const FlashcardSkeleton = () => (
  <div className="w-full max-w-lg mx-auto">
    <div
      className="rounded-2xl p-7 space-y-5"
      style={{
        height: 320,
        background: 'linear-gradient(145deg, rgba(238,242,255,0.6), rgba(224,231,255,0.5))',
        border: '1px solid rgba(99,102,241,0.08)',
      }}
    >
      {/* Badge skeleton */}
      <div className="flex items-center justify-between">
        <div className="w-14 h-5 rounded-lg bg-course-200/40 skeleton-pulse" />
        <div className="w-10 h-4 rounded bg-gray-200/40 skeleton-pulse" />
      </div>

      {/* Question lines skeleton */}
      <div className="flex-1 flex flex-col items-center justify-center gap-3 py-8">
        <div className="w-4/5 h-4 rounded-md bg-course-200/30 skeleton-pulse" />
        <div className="w-3/5 h-4 rounded-md bg-course-200/25 skeleton-pulse" />
        <div className="w-2/5 h-4 rounded-md bg-course-200/20 skeleton-pulse" />
      </div>

      {/* Bottom hint skeleton */}
      <div className="flex justify-center">
        <div className="w-28 h-3 rounded bg-gray-200/30 skeleton-pulse" />
      </div>
    </div>

    {/* Controls skeleton */}
    <div className="flex items-center justify-center gap-4 mt-6">
      <div className="w-20 h-9 rounded-xl bg-gray-200/30 skeleton-pulse" />
      <div className="flex gap-1.5">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="w-2 h-2 rounded-full bg-gray-200/40 skeleton-pulse" />
        ))}
      </div>
      <div className="w-20 h-9 rounded-xl bg-gray-200/30 skeleton-pulse" />
    </div>
  </div>
);

export default FlashcardSkeleton;
