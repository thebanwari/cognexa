/**
 * FlashcardModal — Full-screen overlay with backdrop blur.
 *
 * States:
 *   loading  → skeleton shimmer
 *   error    → retry button
 *   ready    → card + controls
 *
 * Keyboard: ←/→ navigate, Space flip, Esc close
 */
import React, { useState, useEffect, useCallback } from 'react';
import Flashcard from './Flashcard';
import FlashcardControls from './FlashcardControls';
import FlashcardSkeleton from './FlashcardSkeleton';

const FlashcardModal = ({
  isOpen,
  onClose,
  flashcards = [],
  isLoading = false,
  error = null,
  topic = '',
  onRegenerate,
  isRegenerating = false,
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  // Reset when flashcards change
  useEffect(() => {
    setCurrentIndex(0);
    setIsFlipped(false);
  }, [flashcards]);

  // Navigation handlers
  const handleNext = useCallback(() => {
    if (flashcards.length <= 1) return;
    setIsFlipped(false);
    setCurrentIndex((prev) => (prev + 1) % flashcards.length);
  }, [flashcards.length]);

  const handlePrevious = useCallback(() => {
    if (flashcards.length <= 1) return;
    setIsFlipped(false);
    setCurrentIndex((prev) => (prev - 1 + flashcards.length) % flashcards.length);
  }, [flashcards.length]);

  const handleFlip = useCallback(() => {
    setIsFlipped((prev) => !prev);
  }, []);

  // Keyboard navigation
  useEffect(() => {
    if (!isOpen) return;

    const handleKey = (e) => {
      switch (e.key) {
        case 'ArrowRight':
        case 'n':
          e.preventDefault();
          handleNext();
          break;
        case 'ArrowLeft':
        case 'p':
          e.preventDefault();
          handlePrevious();
          break;
        case ' ':
        case 'f':
          e.preventDefault();
          handleFlip();
          break;
        case 'Escape':
          e.preventDefault();
          onClose();
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [isOpen, handleNext, handlePrevious, handleFlip, onClose]);

  if (!isOpen) return null;

  const currentCard = flashcards[currentIndex];

  return (
    <div className="flashcard-modal-backdrop" onClick={onClose}>
      <div
        className="flashcard-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 z-10 p-2 rounded-xl
                     bg-white/60 hover:bg-white/90 border border-gray-200/40
                     transition-all duration-200 group"
          aria-label="Close"
        >
          <svg className="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-course-50/80 border border-course-200/30 mb-3">
            <svg className="w-4 h-4 text-course-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707" />
            </svg>
            <span className="text-[11px] font-semibold text-course-600">AI Flashcards</span>
          </div>
          {topic && (
            <h2 className="text-lg font-bold text-gray-800">{topic}</h2>
          )}
        </div>

        {/* Content area */}
        {isLoading ? (
          <FlashcardSkeleton />
        ) : error ? (
          <div className="text-center py-12">
            <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-red-50 flex items-center justify-center">
              <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-sm font-medium text-gray-700 mb-1">Generation failed</p>
            <p className="text-xs text-gray-400 mb-5">{error}</p>
            <button
              onClick={onRegenerate}
              className="px-5 py-2.5 rounded-xl bg-course-600 hover:bg-course-700 text-white text-sm font-semibold transition-colors"
            >
              Try Again
            </button>
          </div>
        ) : currentCard ? (
          <>
            <Flashcard
              card={currentCard}
              isFlipped={isFlipped}
              onFlip={handleFlip}
              index={currentIndex}
              total={flashcards.length}
            />
            <FlashcardControls
              current={currentIndex}
              total={flashcards.length}
              onPrevious={handlePrevious}
              onNext={handleNext}
              onFlip={handleFlip}
              onRegenerate={onRegenerate}
              isRegenerating={isRegenerating}
            />
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-sm text-gray-400">No flashcards available</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default FlashcardModal;
