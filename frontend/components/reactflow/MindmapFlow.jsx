/**
 * MindmapFlow — Core React Flow component with ELK.js auto-layout.
 *
 * Architecture:
 *   1. Mermaid text → convertMermaidToGraph() → nodes/edges (pos=0,0)
 *   2. computeElkLayout() → nodes with computed positions (LEFT→RIGHT)
 *   3. React Flow renders the layouted graph
 *   4. Expand/collapse → toggle → re-run ELK → smart camera focus
 *
 * Staggered animation: day nodes get --day-index CSS var for cascaded entrance.
 */
import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  Controls,
  Background,
  MiniMap,
  useNodesState,
  useEdgesState,
  useReactFlow,
} from 'reactflow';

import CourseNode from './nodes/CourseNode';
import WeekNode from './nodes/WeekNode';
import DayNode from './nodes/DayNode';
import CustomEdge from './edges/CustomEdge';

import {
  convertMermaidToGraph,
  toggleWeekExpansion,
  getNodeDetails,
} from './utils/convertMermaidToGraph';

import { computeElkLayout } from './utils/elkLayout';

// ── Registries ───────────────────────────────────────────────────
const nodeTypes = {
  courseNode: CourseNode,
  weekNode: WeekNode,
  dayNode: DayNode,
};

const edgeTypes = {
  customEdge: CustomEdge,
};

// ── Layout config ────────────────────────────────────────────────
const ELK_OPTIONS = {
  direction: 'RIGHT',
  nodeSpacing: 28,
  layerSpacing: 170,
  edgeSpacing: 16,
};

const DEFAULT_VIEWPORT = { x: 50, y: 50, zoom: 0.85 };

// ── Inner component ──────────────────────────────────────────────
const MindmapFlowInner = ({ code, height = 780, onNodeClick }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [isLayouting, setIsLayouting] = useState(false);
  const { fitView } = useReactFlow();

  const nodesRef = useRef(nodes);
  const edgesRef = useRef(edges);
  nodesRef.current = nodes;
  edgesRef.current = edges;
  const layoutInProgress = useRef(false);

  // ── Parse mermaid ──────────────────────────────────────────────
  const rawGraph = useMemo(() => {
    if (!code) return { nodes: [], edges: [] };
    try {
      return convertMermaidToGraph(code);
    } catch (err) {
      console.error('convertMermaidToGraph failed:', err);
      return { nodes: [], edges: [] };
    }
  }, [code]);

  // ── Inject toggle + stagger index ─────────────────────────────
  const injectHandlers = useCallback((nodeList, expandedWeekId = null) => {
    let dayIndex = 0;
    return nodeList.map((n) => {
      if (n.type === 'weekNode') {
        return {
          ...n,
          data: { ...n.data, onToggle: (weekId) => handleToggle(weekId) },
        };
      }
      // Stagger: day nodes of the expanded week get incremental --day-index
      // Use a separate style key that won't conflict with RF's positioning
      if (n.type === 'dayNode' && !n.hidden && expandedWeekId && n.data?.weekId === expandedWeekId) {
        const idx = dayIndex++;
        return {
          ...n,
          style: { '--day-index': idx },
        };
      }
      return n;
    });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Run ELK layout ─────────────────────────────────────────────
  const runLayout = useCallback(
    async (nodeList, edgeList, options = {}) => {
      const { animate = true, focusWeekId = null } = options;

      if (layoutInProgress.current) return;
      layoutInProgress.current = true;
      setIsLayouting(true);

      try {
        const { nodes: layouted } = await computeElkLayout(
          nodeList, edgeList, ELK_OPTIONS
        );

        const withHandlers = injectHandlers(layouted, focusWeekId);
        setNodes(withHandlers);
        setEdges(edgeList);

        // Smart camera
        setTimeout(() => {
          try {
            if (focusWeekId) {
              const dayIds = withHandlers
                .filter(n => n.type === 'dayNode' && n.data?.weekId === focusWeekId && !n.hidden)
                .map(n => n.id);

              if (dayIds.length > 0) {
                fitView({
                  nodes: [{ id: focusWeekId }, ...dayIds.map(id => ({ id }))],
                  padding: 0.4,
                  maxZoom: 0.95,
                  duration: 650,
                });
                return;
              }
            }
            fitView({
              padding: 0.2,
              maxZoom: 1.1,
              duration: animate ? 550 : 0,
            });
          } catch (_) {}
        }, animate ? 90 : 10);
      } catch (err) {
        console.error('ELK layout failed:', err);
        setNodes(injectHandlers(nodeList));
        setEdges(edgeList);
      } finally {
        setIsLayouting(false);
        layoutInProgress.current = false;
      }
    },
    [fitView, injectHandlers, setNodes, setEdges]
  );

  // ── Toggle handler ─────────────────────────────────────────────
  const handleToggle = useCallback((weekId) => {
    const currentNodes = nodesRef.current;
    const currentEdges = edgesRef.current;

    const weekNode = currentNodes.find(n => n.id === weekId && n.type === 'weekNode');
    const isExpanding = weekNode?.data?.isCollapsed === true;

    const { nodes: toggled, edges: toggledEdges } = toggleWeekExpansion(
      currentNodes, currentEdges, weekId
    );

    runLayout(toggled, toggledEdges, {
      animate: true,
      focusWeekId: isExpanding ? weekId : null,
    });
  }, [runLayout]);

  // ── Initial layout ─────────────────────────────────────────────
  useEffect(() => {
    if (rawGraph.nodes.length === 0) return;
    runLayout(rawGraph.nodes, rawGraph.edges, { animate: false });
  }, [rawGraph]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Node click → sidebar ───────────────────────────────────────
  const handleNodeClick = useCallback(
    (_evt, node) => {
      const info = getNodeDetails(node.id, nodesRef.current);
      if (typeof onNodeClick === 'function') onNodeClick(info);
    },
    [onNodeClick]
  );

  // ── MiniMap colors ─────────────────────────────────────────────
  const miniMapColor = useCallback((node) => {
    switch (node.type) {
      case 'courseNode': return '#a5b4fc';
      case 'weekNode':  return '#86efac';
      case 'dayNode':   return '#fde68a';
      default:          return '#e2e8f0';
    }
  }, []);

  return (
    <div className="relative w-full" style={{ height }}>
      {/* Loading — initial only */}
      {isLayouting && nodes.length === 0 && (
        <div className="absolute inset-0 z-30 flex items-center justify-center bg-white/40 backdrop-blur-sm">
          <div className="flex items-center gap-3 px-5 py-3 rounded-2xl bg-white/90 shadow-xl border border-gray-100/50">
            <div className="w-4 h-4 border-2 border-course-500 border-t-transparent rounded-full animate-spin" />
            <span className="text-sm font-medium text-gray-500">Computing layout…</span>
          </div>
        </div>
      )}

      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={handleNodeClick}
        defaultViewport={DEFAULT_VIEWPORT}
        fitView={false}
        panOnScroll
        zoomOnScroll
        panOnDrag
        minZoom={0.1}
        maxZoom={2}
        proOptions={{ hideAttribution: true }}
        className="mindmap-canvas"
        nodesDraggable={false}
      >
        <Background
          variant="dots"
          gap={36}
          size={0.8}
          color="#c7d2fe"
          style={{ opacity: 0.15 }}
        />

        <MiniMap
          nodeColor={miniMapColor}
          maskColor="rgba(148, 163, 184, 0.08)"
          pannable
          zoomable
          position="bottom-right"
          style={{ width: 130, height: 80 }}
        />

        <Controls
          showZoom
          showFitView
          showInteractive={false}
          position="bottom-left"
        />
      </ReactFlow>
    </div>
  );
};

const MindmapFlow = (props) => (
  <ReactFlowProvider>
    <MindmapFlowInner {...props} />
  </ReactFlowProvider>
);

export default MindmapFlow;