import { useState } from "react";

export default function MindmapViewer({ mermaidText, imageUrl }) {
  const [showMermaid, setShowMermaid] = useState(false);

  // Convert relative URL → absolute backend URL
  const fixedUrl = imageUrl ? `http://localhost:8000${imageUrl}` : null;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4 text-center">Mindmap Viewer</h1>

      {/* Mindmap Image */}
      <div className="border p-4 rounded-xl shadow bg-white">
        <h2 className="text-xl font-semibold mb-2">Generated Mindmap</h2>

        {fixedUrl ? (
          <img
            src={fixedUrl}
            alt="Mindmap"
            className="w-full rounded-lg border shadow"
          />
        ) : (
          <p className="text-red-500">No image found.</p>
        )}
      </div>

      {/* Toggle Mermaid Code */}
      <button
        onClick={() => setShowMermaid(!showMermaid)}
        className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
      >
        {showMermaid ? "Hide Mermaid Code" : "Show Mermaid Code"}
      </button>

      {showMermaid && (
        <pre className="mt-3 p-4 bg-gray-900 text-green-300 rounded-lg overflow-auto text-sm">
{mermaidText}
        </pre>
      )}

      {/* Download button */}
      {fixedUrl && (
        <a
          download
          href={fixedUrl}
          className="mt-4 inline-block px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
        >
          Download PNG
        </a>
      )}
    </div>
  );
}
