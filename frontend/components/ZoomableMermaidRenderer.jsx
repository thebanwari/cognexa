import { useState, useEffect, useRef, useCallback } from 'react';
import { TransformWrapper, TransformComponent } from 'react-zoom-pan-pinch';

export default function ZoomableMermaidRenderer({ code, className = '', theme = 'default', themeVariables = {}, height = 600 }) {
  const svgContainerRef = useRef(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [mermaidInstance, setMermaidInstance] = useState(null);

  // Initialize Mermaid once
  const initializeMermaid = useCallback(async () => {
    if (typeof window === 'undefined') return;

    try {
      const mermaidModule = await import('mermaid');
      const mermaid = mermaidModule.default;

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
        fontFamily: 'Inter, sans-serif',
      });

      setMermaidInstance(mermaid);
      setIsInitialized(true);
    } catch (err) {
      console.error('Failed to initialize Mermaid:', err);
      setError('Failed to initialize Mermaid renderer');
    }
  }, [theme, themeVariables]);

  // Render diagram function
  const renderDiagram = useCallback(async () => {
    if (!isInitialized || !mermaidInstance || !code || !svgContainerRef.current) return;

    setIsLoading(true);
    setError(null);

    try {
      // Clear previous diagram
      svgContainerRef.current.innerHTML = '';

      // Generate unique ID for this render
      const renderId = `mermaid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

      // Render the diagram
      const { svg } = await mermaidInstance.render(renderId, code);

      // Directly set the SVG content using innerHTML
      svgContainerRef.current.innerHTML = svg;

      // Ensure SVG is responsive
      const svgElement = svgContainerRef.current.querySelector('svg');
      if (svgElement) {
        svgElement.style.width = '100%';
        svgElement.style.height = 'auto';
        svgElement.style.maxWidth = '100%';
        svgElement.style.display = 'block';
        svgElement.style.margin = '0 auto';
        svgElement.setAttribute('preserveAspectRatio', 'xMidYMid meet');

        // Add some minimum height for better visibility
        svgElement.style.minHeight = '400px';
      }

      setIsLoading(false);
    } catch (err) {
      console.error('Failed to render Mermaid diagram:', err);
      console.error('Mermaid code:', code);
      setError('Failed to render diagram. Check console for details.');
      setIsLoading(false);
    }
  }, [isInitialized, mermaidInstance, code]);

  // Download SVG functionality
  const downloadSVG = useCallback(() => {
    if (!svgContainerRef.current) return;

    const svgElement = svgContainerRef.current.querySelector('svg');
    if (!svgElement) return;

    try {
      // Get the outer HTML of the SVG element
      const svgData = new XMLSerializer().serializeToString(svgElement);
      const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });

      // Create download link
      const downloadLink = document.createElement('a');
      downloadLink.href = URL.createObjectURL(svgBlob);
      downloadLink.download = `course-mindmap-${Date.now()}.svg`;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    } catch (err) {
      console.error('Failed to download SVG:', err);
      setError('Failed to download SVG');
    }
  }, []);

  // Initialize Mermaid on mount
  useEffect(() => {
    initializeMermaid();
  }, [initializeMermaid]);

  // Render diagram when code or initialization changes
  useEffect(() => {
    if (isInitialized && mermaidInstance && code) {
      renderDiagram();
    }
  }, [isInitialized, mermaidInstance, code, renderDiagram]);

  // Show error if any
  if (error) {
    return (
      <div className={`bg-red-50 border border-red-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center justify-between">
          <div className="text-red-800 font-medium">{error}</div>
          <button
            onClick={() => {
              setError(null);
              if (code) renderDiagram();
            }}
            className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`zoomable-mermaid-container relative ${className}`} style={{ height }}>
      {/* Controls - only show when diagram is available */}
      {isInitialized && code && (
        <div className="absolute top-4 right-4 z-20 flex gap-2">
          <button
            onClick={downloadSVG}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2 shadow-lg hover:scale-105"
            title="Download SVG"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Download SVG
          </button>
        </div>
      )}

      {/* Loading Overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-white bg-opacity-90 flex items-center justify-center z-10 rounded-lg">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600 mx-auto mb-3"></div>
            <div className="text-gray-600 text-sm font-medium">Rendering mindmap...</div>
          </div>
        </div>
      )}

      {/* Zoom and Pan Container */}
      <TransformWrapper
        initialScale={1}
        minScale={0.1}
        maxScale={3}
        wheel={{ step: 0.1, smoothStep: true }}
        panning={{ locked: false }}
        doubleClick={{ mode: 'reset' }}
        zoomAnimation={{ disabled: false, velocityDisabled: false }}
        centerView={{ padding: 0 }}
      >
        {({ zoomIn, zoomOut, resetTransform, ...rest }) => (
          <>
            {/* Zoom Controls */}
            <div className="absolute top-4 left-4 z-20 flex flex-col gap-2 bg-white bg-opacity-95 rounded-lg shadow-xl p-2">
              <button
                onClick={() => zoomIn()}
                className="w-8 h-8 bg-blue-600 hover:bg-blue-700 text-white rounded flex items-center justify-center transition-all duration-200 hover:scale-105 active:scale-95"
                title="Zoom In (Ctrl + Scroll Up)"
              >
                <span className="text-xs font-bold">+</span>
              </button>
              <button
                onClick={() => zoomOut()}
                className="w-8 h-8 bg-blue-600 hover:bg-blue-700 text-white rounded flex items-center justify-center transition-all duration-200 hover:scale-105 active:scale-95"
                title="Zoom Out (Ctrl + Scroll Down)"
              >
                <span className="text-xs font-bold">-</span>
              </button>
              <div className="border-t border-gray-200 my-1"></div>
              <button
                onClick={() => resetTransform()}
                className="w-8 h-8 bg-gray-600 hover:bg-gray-700 text-white rounded flex items-center justify-center transition-all duration-200 hover:scale-105 active:scale-95"
                title="Reset Zoom"
              >
                <svg className="w-3.5 h-3.5 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m0 0H9m11 11V4a1 1 0 00-1-1h-5a1 1 0 00-1 1v5H3a1 1 0 01-1-1v-9a1 1 0 001-1h14a1 1 0 011 1v9a1 1 0 00-1 1h-5a1 1 0 00-1-1h5a1 1 0 01-1 1m-8 5a1 1 0 00-1 1v-7a1 1 0 001-1h14a1 1 0 001-1v7a1 1 0 00-1 1m0 0H9m7-5V4a1 1 0 00-1-1H8a1 1 0 00-1 1v5H3a1 1 0 01-1-1v-9a1 1 0 001-1h14a1 1 0 011 1v9a1 1 0 00-1 1h-5a1 1 0 00-1-1h-5a1 1 0 00-1 1v-7a1 1 0 001-1h5a1 1 0 001 1v7m0 0H9m7-5V4a1 1 0 00-1-1H8a1 1 0 00-1 1v5" />
                </svg>
              </button>
            </div>

            <TransformComponent
              wrapperClass="w-full h-full"
              contentClass="w-full h-full flex items-center justify-center"
            >
              {/* SVG Container - This is where the magic happens */}
              <div
                ref={svgContainerRef}
                className="mermaid w-full h-full flex items-center justify-center min-h-[400px] px-4"
                style={{
                  minHeight: '400px',
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                {/* Show loading state when initializing */}
                {!code ? (
                  <div className="text-center py-12 text-gray-500">
                    <div className="text-lg font-medium mb-2">No diagram code provided</div>
                    <div className="text-sm">Generate a course to view the mindmap</div>
                  </div>
                ) : !isInitialized ? (
                  <div className="text-center py-12">
                    <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600 mx-auto mb-3"></div>
                    <div className="text-gray-500 text-sm">Initializing Mermaid renderer...</div>
                  </div>
                ) : isLoading ? (
                  <div className="text-center py-12">
                    <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600 mx-auto mb-3"></div>
                    <div className="text-gray-500 text-sm">Rendering diagram...</div>
                  </div>
                ) : (
                  <div className="text-center py-12 text-gray-500">
                    <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-gray-400 mx-auto mb-3"></div>
                    <div className="text-sm">Processing...</div>
                  </div>
                )}
              </div>
            </TransformComponent>
          </>
        )}
      </TransformWrapper>
    </div>
  );
}