import { useState } from "react";
import { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();
  const [sessionId, setSessionId] = useState("");

  const handleCreateCourse = () => {
    if (sessionId.trim()) {
      router.push(`/course-builder?session_id=${sessionId}`);
    } else {
      // Generate a new session ID
      const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      router.push(`/course-builder?session_id=${newSessionId}`);
    }
  };

  const handleViewMindmap = () => {
    if (sessionId.trim()) {
      router.push(`/mindmap/${sessionId}`);
    } else {
      alert("Please enter a session ID to view mindmap");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-gray-900">CourseCraft-AI</h1>
          <p className="text-gray-600 mt-1">Create professional course mindmaps with AI</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <div className="text-center">
          {/* Logo/Icon */}
          <div className="mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl shadow-lg">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 14.523 5.754 14 7.5 14s3.332.523 4.5 1.253M12 6.253c1.168 0 2.754-.477 4.5-1.253v13C17.668 14.523 16.082 14 14.5 14 12.746 14 11.168 14.523 10 15.247" />
              </svg>
            </div>
          </div>

          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            AI-Powered Course Mindmap Generator
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Transform your course content into beautiful, interactive mindmaps.
            Generate professional visualizations that help students understand
            course structure and relationships between concepts.
          </p>

          {/* Session Input */}
          <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-200">
            <div className="mb-4">
              <label htmlFor="session" className="block text-sm font-medium text-gray-700 mb-2">
                Session ID (Optional)
              </label>
              <input
                id="session"
                type="text"
                value={sessionId}
                onChange={(e) => setSessionId(e.target.value)}
                placeholder="Enter existing session ID or leave empty for new session"
                className="w-full max-w-md px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-4 sm:space-y-0 sm:space-x-4 flex flex-col sm:flex-row items-center justify-center">
            <button
              onClick={handleCreateCourse}
              className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-4 px-8 rounded-xl hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <svg className="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create New Course
            </button>

            <button
              onClick={handleViewMindmap}
              className="bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold py-4 px-8 rounded-xl hover:from-green-700 hover:to-emerald-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <svg className="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7z" />
              </svg>
              View Existing Mindmap
            </button>
          </div>

          {/* Features */}
          <div className="mt-16 grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
              <div className="text-blue-600 mb-4">
                <svg className="w-10 h-10 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.364-.707.707M21 12h-1M4 12H3m3.343-5.657-.707-.707M18.364 18.364-.707-.707" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Professional Quality</h3>
              <p className="text-gray-600 text-sm">HD PNG and SVG exports with professional styling and layout</p>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
              <div className="text-indigo-600 mb-4">
                <svg className="w-10 h-10 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Interactive Viewer</h3>
              <p className="text-gray-600 text-sm">Zoom, pan, and explore your mindmaps with smooth interactions</p>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
              <div className="text-purple-600 mb-4">
                <svg className="w-10 h-10 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI-Powered</h3>
              <p className="text-gray-600 text-sm">Smart layout generation and content organization</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}