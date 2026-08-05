import { useState, useEffect, useRef } from 'react';

export default function MermaidRenderer({ code, className = '', theme = 'default', themeVariables = {} }) {
  const containerRef = useRef(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState(null);

  const initializeMermaid = async () => {
    if (typeof window === 'undefined') return;

    try {
      const mermaid = require('mermaid');

      const defaultThemeVariables = {
        primaryColor: '#2563eb',
        primaryBorderColor: '#1d4ed8',
        lineColor: '#6b7280',
        fontSize: '16px',
        fontFamily: 'Inter, sans-serif',
        secondaryColor: '#f1f5f9',
        tertiaryColor: '#1e293b',
        primaryTextColor: '#ffffff',
        secondaryTextColor: '#64748b',
        background: '#ffffff',
        mainBkg: '#2563eb',
        secondBkg: '#059669',
        tertiaryBkg: '#d97706',
        ...themeVariables,
      };

      mermaid.initialize({
        startOnLoad: false,
        theme: theme,
        themeVariables: defaultThemeVariables,
        flowchart: {
          useMaxWidth: true,
          htmlLabels: true,
          curve: 'basis',
        },
        securityLevel: 'loose',
      });

      setIsInitialized(true);
    } catch (err) {
      console.error('Failed to initialize Mermaid:', err);
      setError('Failed to initialize Mermaid renderer');
    }
  };

  const renderDiagram = async () => {
    if (!isInitialized || !code || !containerRef.current) return;

    try {
      const mermaid = require('mermaid');

      // Clear previous diagram
      containerRef.current.innerHTML = '';

      // Render new diagram
      const { svg } = await mermaid.render(`mermaid-${Date.now()}`, code);

      // Set the SVG content
      containerRef.current.innerHTML = svg;

      // Add responsive styling
      const svgElement = containerRef.current.querySelector('svg');
      if (svgElement) {
        svgElement.style.maxWidth = '100%';
        svgElement.style.height = 'auto';
        svgElement.style.display = 'block';
        svgElement.style.margin = '0 auto';
      }

      setError(null);
    } catch (err) {
      console.error('Failed to render Mermaid diagram:', err);
      setError('Failed to render diagram');
    }
  };

  useEffect(() => {
    initializeMermaid();
  }, []);

  useEffect(() => {
    if (isInitialized && code) {
      renderDiagram();
    }
  }, [isInitialized, code]);

  if (error) {
    return (
      <div className={`bg-red-50 border border-red-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center justify-between">
          <div className="text-red-800">{error}</div>
          <button
            onClick={() => window.location.reload()}
            className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className={`mermaid-renderer ${className}`}
      style={{
        minHeight: '300px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {!code ? (
        <div className="text-center py-8 text-gray-500">
          No diagram code provided
        </div>
      ) : !isInitialized ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <div className="text-gray-500">Initializing Mermaid renderer...</div>
        </div>
      ) : null}
    </div>
  );
}