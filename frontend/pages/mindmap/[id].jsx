import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import MindmapFlow from '../../components/reactflow/MindmapFlow';
import Sidebar from '../../components/reactflow/Sidebar';
import FlashcardModal from '../../components/flashcards/FlashcardModal';

export default function MindmapPage() {
  const router = useRouter();
  const { id: session_id } = router.query;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [mermaidText, setMermaidText] = useState('');
  const [selectedNode, setSelectedNode] = useState(null);

  // Flashcard states
  const [isFlashcardModalOpen, setIsFlashcardModalOpen] = useState(false);
  const [flashcardsData, setFlashcardsData] = useState([]);
  const [flashcardsTopic, setFlashcardsTopic] = useState('');
  const [isFlashcardsLoading, setIsFlashcardsLoading] = useState(false);
  const [flashcardsError, setFlashcardsError] = useState(null);

  /* ── Fetch mindmap data ─────────────────────────────────────── */
  const generateMindmap = async () => {
    if (!session_id) return;
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('http://localhost:8000/api/v1/mindmap/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      if (data.success) {
        setMermaidText(data.mermaid_text || '');
      } else {
        throw new Error(data.message || 'Failed to generate mindmap');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    generateMindmap();
  }, [session_id]); // eslint-disable-line react-hooks/exhaustive-deps

  /* ── Fetch flashcards ───────────────────────────────────────── */
  const generateFlashcards = async (topic) => {
    if (!session_id) return;
    
    setFlashcardsTopic(topic);
    setIsFlashcardModalOpen(true);
    setIsFlashcardsLoading(true);
    setFlashcardsError(null);

    try {
      const res = await fetch('http://localhost:8000/api/v1/flashcards/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id, topic, difficulty: 'beginner' }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      if (data.success) {
        setFlashcardsData(data.flashcards || []);
      } else {
        throw new Error(data.message || 'Failed to generate flashcards');
      }
    } catch (err) {
      setFlashcardsError(err.message);
    } finally {
      setIsFlashcardsLoading(false);
    }
  };

  /* ── Loading state ──────────────────────────────────────────── */
  if (loading) {
    return (
      <>
        <Head><title>Loading Mindmap… | CourseCraft-AI</title></Head>
        <div className="h-screen flex items-center justify-center bg-canvas-50">
          <div className="text-center">
            <div className="relative mx-auto w-14 h-14 mb-5">
              <div className="absolute inset-0 rounded-full border-[3px] border-course-200" />
              <div className="absolute inset-0 rounded-full border-[3px] border-course-500 border-t-transparent animate-spin" />
            </div>
            <p className="text-gray-700 font-semibold text-lg">Generating Mindmap…</p>
            <p className="text-gray-400 text-sm mt-1">Laying out your course structure</p>
          </div>
        </div>
      </>
    );
  }

  /* ── Error state ────────────────────────────────────────────── */
  if (error) {
    return (
      <>
        <Head><title>Error | CourseCraft-AI</title></Head>
        <div className="h-screen flex items-center justify-center bg-canvas-50">
          <div className="max-w-sm text-center bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
            <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-red-50 flex items-center justify-center">
              <svg className="w-7 h-7 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Generation Failed</h2>
            <p className="text-gray-500 text-sm mb-6">{error}</p>
            <div className="flex gap-3">
              <button
                onClick={generateMindmap}
                className="flex-1 px-4 py-2.5 rounded-xl bg-course-600 hover:bg-course-700 text-white text-sm font-semibold transition-colors"
              >
                Retry
              </button>
              <button
                onClick={() => router.push('/')}
                className="flex-1 px-4 py-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold transition-colors"
              >
                Home
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  /* ── Main mindmap view ──────────────────────────────────────── */
  return (
    <>
      <Head>
        <title>Course Mindmap | CourseCraft-AI</title>
        <meta name="description" content="Interactive course mindmap visualization" />
      </Head>

      <div className="h-screen flex flex-col bg-canvas-50 overflow-hidden">
        {/* ── Top bar ──────────────────────────────────────────── */}
        <header className="flex items-center justify-between px-6 py-3 bg-white/80 backdrop-blur-md border-b border-gray-200/60 z-20 shrink-0">
          <div className="flex items-center gap-3">
            {/* Logo */}
            <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-course-500 to-course-700 shadow-sm">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.364-.707.707M21 12h-1M4 12H3m3.343-5.657-.707-.707M18.364 18.364-.707-.707" />
              </svg>
            </div>
            <div>
              <h1 className="text-base font-bold text-gray-900 leading-tight">Course Mindmap</h1>
              <p className="text-[11px] text-gray-400 font-mono">
                {session_id ? session_id.slice(0, 20) + '…' : '—'}
              </p>
            </div>
          </div>

          {/* Legend */}
          <div className="hidden sm:flex items-center gap-4 text-[11px] text-gray-500">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-course-400" /> Course
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-week-400" /> Week
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-day-400" /> Day
            </span>
            <span className="text-gray-300">|</span>
            <span>Click nodes to explore • Expand weeks with ▶</span>
          </div>

          {/* Actions */}
          <button
            onClick={() => router.push('/')}
            className="px-3 py-1.5 rounded-lg text-xs font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
          >
            ← Back
          </button>
        </header>

        {/* ── Canvas + Sidebar ─────────────────────────────────── */}
        <div className="flex-1 flex min-h-0">
          {/* Flow canvas */}
          <div className="flex-1 min-w-0">
            <MindmapFlow
              code={mermaidText}
              onNodeClick={(details) => setSelectedNode(details)}
              height="100%"
            />
          </div>

          {/* Sidebar (slide-in) */}
          {selectedNode && (
            <div className="sidebar-enter shrink-0">
              <Sidebar
                selectedNodeDetails={selectedNode}
                onClose={() => setSelectedNode(null)}
                onGenerateFlashcards={generateFlashcards}
              />
            </div>
          )}
        </div>
      </div>

      {/* ── Flashcard Modal Overlay ────────────────────────────── */}
      <FlashcardModal
        isOpen={isFlashcardModalOpen}
        onClose={() => setIsFlashcardModalOpen(false)}
        flashcards={flashcardsData}
        isLoading={isFlashcardsLoading}
        error={flashcardsError}
        topic={flashcardsTopic}
        onRegenerate={() => generateFlashcards(flashcardsTopic)}
        isRegenerating={isFlashcardsLoading}
      />
    </>
  );
}