import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Head from "next/head";
import AssignmentViewer from "../../components/AssignmentViewer";
import FlashcardViewer from "../../components/FlashcardViewer";

export default function CoursePage() {
  const router = useRouter();
  const { id: session_id } = router.query;

  // PDF State
  const [pdfLoading, setPdfLoading] = useState(false);
  const [pdfError, setPdfError] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);

  // Assignment State
  const [assignmentLoading, setAssignmentLoading] = useState(false);
  const [assignmentError, setAssignmentError] = useState(null);
  const [assignments, setAssignments] = useState([]);

  // Flashcard State
  const [flashcardLoading, setFlashcardLoading] = useState(false);
  const [flashcardError, setFlashcardError] = useState(null);
  const [flashcards, setFlashcards] = useState([]);

  const generatePdf = async () => {
    if (!session_id || pdfLoading) return;

    setPdfLoading(true);
    setPdfError(null);

    try {
      const response = await fetch("http://localhost:8000/api/v1/generate-pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ session_id }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success && data.pdf_url) {
        setPdfUrl(data.pdf_url);
        setPdfLoading(false);
      } else {
        throw new Error(data.message || "Failed to generate PDF");
      }
    } catch (err) {
      setPdfError(err.message);
      setPdfLoading(false);
    }
  };

  const generateAssignments = async () => {
    if (!session_id || assignmentLoading) return;

    setAssignmentLoading(true);
    setAssignmentError(null);

    try {
      const response = await fetch("http://localhost:8000/api/v1/assignments/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ session_id }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success && data.assignments) {
        setAssignments(data.assignments);
        setAssignmentLoading(false);
      } else {
        throw new Error(data.message || "Failed to generate assignments");
      }
    } catch (err) {
      setAssignmentError(err.message);
      setAssignmentLoading(false);
    }
  };

  const generateFlashcards = async () => {
    if (!session_id || flashcardLoading) return;

    setFlashcardLoading(true);
    setFlashcardError(null);

    try {
      const response = await fetch("http://localhost:8000/api/v1/flashcards/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ session_id }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success && data.flashcards) {
        setFlashcards(data.flashcards);
        setFlashcardLoading(false);
      } else {
        throw new Error(data.message || "Failed to generate flashcards");
      }
    } catch (err) {
      setFlashcardError(err.message);
      setFlashcardLoading(false);
    }
  };

  const handleDownload = () => {
    if (!pdfUrl) return;

    // Open PDF in new tab
    const fullUrl = `http://localhost:8000${pdfUrl}`;
    window.open(fullUrl, '_blank');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <Head>
        <title>Course PDF Generator | CourseCraft-AI</title>
        <meta name="description" content="Generate and download course PDF" />
      </Head>

      <div className="container mx-auto px-6 py-12">
        {/* Header */}
        <div className="max-w-4xl mx-auto text-center mb-12">
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
            <div className="flex items-center justify-center mb-4">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Course PDF Generator</h1>
            <p className="text-gray-600 text-lg">Session: <span className="font-mono bg-gray-100 px-3 py-1 rounded-lg text-sm">{session_id || 'Loading...'}</span></p>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200">

            {/* Action Buttons Section */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Generate PDF Button */}
              <button
                onClick={generatePdf}
                disabled={pdfLoading || !session_id}
                className={`p-6 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105 focus:outline-none ${
                  pdfLoading || !session_id
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-br from-blue-600 to-blue-700 text-white shadow-lg hover:shadow-xl'
                }`}
              >
                {pdfLoading ? (
                  <div className="flex flex-col items-center space-y-2">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                    <span className="text-sm">Generating...</span>
                  </div>
                ) : (
                  <div className="flex flex-col items-center space-y-2">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span>Generate PDF</span>
                  </div>
                )}
              </button>

              {/* Generate Assignments Button */}
              <button
                onClick={generateAssignments}
                disabled={assignmentLoading || !session_id}
                className={`p-6 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105 focus:outline-none ${
                  assignmentLoading || !session_id
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-br from-green-600 to-green-700 text-white shadow-lg hover:shadow-xl'
                }`}
              >
                {assignmentLoading ? (
                  <div className="flex flex-col items-center space-y-2">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                    <span className="text-sm">Generating...</span>
                  </div>
                ) : (
                  <div className="flex flex-col items-center space-y-2">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span>Generate Assignments</span>
                  </div>
                )}
              </button>

              {/* Generate Flashcards Button */}
              <button
                onClick={generateFlashcards}
                disabled={flashcardLoading || !session_id}
                className={`p-6 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105 focus:outline-none ${
                  flashcardLoading || !session_id
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-br from-purple-600 to-purple-700 text-white shadow-lg hover:shadow-xl'
                }`}
              >
                {flashcardLoading ? (
                  <div className="flex flex-col items-center space-y-2">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                    <span className="text-sm">Generating...</span>
                  </div>
                ) : (
                  <div className="flex flex-col items-center space-y-2">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    <span>Generate Flashcards</span>
                  </div>
                )}
              </button>
            </div>

            {/* Error Messages */}
            {(pdfError || assignmentError || flashcardError) && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{pdfError || assignmentError || flashcardError}</span>
                </div>
              </div>
            )}

            {/* PDF Success State */}
            {pdfUrl && !pdfLoading && !pdfError && (
              <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span>PDF generated successfully!</span>
                  </div>
                  <button
                    onClick={handleDownload}
                    className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors transform hover:scale-105"
                  >
                    Download PDF
                  </button>
                </div>
              </div>
            )}

            {/* Assignment Viewer */}
            {assignments.length > 0 && !assignmentLoading && !assignmentError && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Generated Assignments</h3>
                <AssignmentViewer assignments={assignments} />
              </div>
            )}

            {/* Flashcard Viewer */}
            {flashcards.length > 0 && !flashcardLoading && !flashcardError && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Generated Flashcards</h3>
                <FlashcardViewer flashcards={flashcards} />
              </div>
            )}

            {/* Instructions */}
            <div className="mt-8 p-6 bg-gray-50 rounded-xl">
              <h3 className="text-lg font-medium text-gray-900 mb-2">How it works:</h3>
              <ul className="text-gray-600 space-y-1 text-sm">
                <li>• Click "Generate PDF" to create your course PDF</li>
                <li>• Click "Generate Assignments" for practice questions</li>
                <li>• Click "Generate Flashcards" for quick review cards</li>
                <li>• Wait for generation to complete</li>
                <li>• PDFs open in new tab, assignments and flashcards display below</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}