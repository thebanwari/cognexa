import React, { useState } from 'react';

const FlashcardViewer = ({ flashcards }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  if (!flashcards || flashcards.length === 0) {
    return null;
  }

  const currentCard = flashcards[currentIndex];

  const handleNext = () => {
    setIsFlipped(false);
    setCurrentIndex((prev) => (prev + 1) % flashcards.length);
  };

  const handlePrevious = () => {
    setIsFlipped(false);
    setCurrentIndex((prev) => (prev - 1 + flashcards.length) % flashcards.length);
  };

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
  };

  const handleKeyPress = (e) => {
    switch (e.key) {
      case 'ArrowRight':
      case 'n':
        handleNext();
        break;
      case 'ArrowLeft':
      case 'p':
        handlePrevious();
        break;
      case ' ':
      case 'f':
        handleFlip();
        break;
      default:
        break;
    }
  };

  React.useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentIndex, isFlipped]);

  return (
    <div className="space-y-4">
      {/* Flashcard Display */}
      <div
        className="relative w-full max-w-2xl mx-auto perspective-1000 cursor-pointer"
        onClick={handleFlip}
      >
        <div
          className={`relative w-full h-64 bg-white rounded-xl shadow-lg border border-gray-200 [transform-style:preserve-3d] transition-transform duration-600 ${
            isFlipped ? '[transform:rotateY(180deg)]' : ''
          }`}
        >
          {/* Front of Card */}
          <div className="absolute inset-0 [backface-visibility:hidden] rounded-xl">
            <div className="h-full p-6 flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 bg-gradient-to-r from-purple-500 to-purple-600 text-white text-sm font-medium rounded-full">
                  Front
                </span>
                <span className="text-sm text-gray-500">
                  {currentIndex + 1} / {flashcards.length}
                </span>
              </div>
              <div className="flex-1 flex items-center justify-center">
                <p className="text-lg font-semibold text-gray-900 text-center leading-relaxed">
                  {currentCard.front}
                </p>
              </div>
              <div className="text-center text-sm text-gray-500 mt-2">
                Click to flip or use keyboard: ← → Space
              </div>
            </div>
          </div>

          {/* Back of Card */}
          <div className="absolute inset-0 backface-hidden rotate-y-180 rounded-xl">
            <div className="h-full p-6 flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <span className="px-3 py-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white text-sm font-medium rounded-full">
                  Back
                </span>
                <span className="text-sm text-gray-500">
                  {currentIndex + 1} / {flashcards.length}
                </span>
              </div>
              <div className="flex-1 flex items-center justify-center">
                <p className="text-lg text-gray-800 text-center leading-relaxed">
                  {currentCard.back}
                </p>
              </div>
              <div className="text-center text-sm text-gray-500 mt-2">
                Click to flip back or use Space
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="flex items-center justify-center space-x-4">
        <button
          onClick={handlePrevious}
          disabled={flashcards.length <= 1}
          className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          <span>Previous</span>
        </button>

        <div className="flex space-x-2">
          {flashcards.map((_, index) => (
            <button
              key={index}
              onClick={() => {
                setIsFlipped(false);
                setCurrentIndex(index);
              }}
              className={`w-3 h-3 rounded-full transition-colors ${
                index === currentIndex
                  ? 'bg-purple-500 ring-2 ring-purple-300'
                  : 'bg-gray-300 hover:bg-gray-400'
              }`}
              title={`Card ${index + 1}`}
            />
          ))}
        </div>

        <button
          onClick={handleNext}
          disabled={flashcards.length <= 1}
          className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>Next</span>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Keyboard Shortcuts */}
      <div className="text-center text-sm text-gray-500">
        <div className="flex justify-center space-x-4">
          <span>← Previous | → Next | Space Flip</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-gradient-to-r from-purple-500 to-purple-600 h-2 rounded-full transition-all duration-300"
          style={{
            width: `${((currentIndex + 1) / flashcards.length) * 100}%`
          }}
        />
      </div>
    </div>
  );
};

export default FlashcardViewer;
