/**
 * ELK.js Layout Engine for React Flow
 *
 * Computes hierarchical LEFT-TO-RIGHT layout using Eclipse Layout Kernel.
 * Converts React Flow nodes/edges to ELK graph, runs layout, and maps
 * computed positions back to React Flow format.
 */
import ELK from 'elkjs/lib/elk.bundled.js';

const elk = new ELK();

// Default dimensions per node type
const NODE_DIMENSIONS = {
  courseNode: { width: 360, height: 130 },
  weekNode:  { width: 230, height: 90 },
  dayNode:   { width: 210, height: 85 },
  default:   { width: 210, height: 80 },
};

/**
 * Compute ELK layout for React Flow nodes and edges.
 *
 * @param {Array} nodes   – React Flow nodes (visible ones only)
 * @param {Array} edges   – React Flow edges
 * @param {Object} options – Layout options
 * @returns {Promise<{nodes: Array, edges: Array}>}
 */
export async function computeElkLayout(nodes, edges, options = {}) {
  const {
    direction = 'RIGHT',          // LEFT-TO-RIGHT tree
    nodeSpacing = 28,             // vertical gap between siblings (tighter)
    layerSpacing = 180,           // horizontal gap between layers
    edgeSpacing = 20,             // gap between parallel edges
  } = options;

  // Filter to only visible nodes
  const visibleNodes = nodes.filter(n => !n.hidden);
  const visibleNodeIds = new Set(visibleNodes.map(n => n.id));

  // Filter edges to only those connecting visible nodes
  const visibleEdges = edges.filter(
    e => visibleNodeIds.has(e.source) && visibleNodeIds.has(e.target)
  );

  // Build ELK graph
  const elkGraph = {
    id: 'root',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': direction,
      'elk.spacing.nodeNode': String(nodeSpacing),
      'elk.layered.spacing.nodeNodeBetweenLayers': String(layerSpacing),
      'elk.layered.spacing.edgeEdgeBetweenLayers': String(edgeSpacing),
      'elk.layered.spacing.edgeNodeBetweenLayers': String(edgeSpacing),
      'elk.edgeRouting': 'SPLINES',
      'elk.layered.nodePlacement.strategy': 'NETWORK_SIMPLEX',
      'elk.layered.crossingMinimization.strategy': 'LAYER_SWEEP',
      'elk.spacing.componentComponent': '60',
      'elk.layered.considerModelOrder.strategy': 'NODES_AND_EDGES',
    },
    children: visibleNodes.map(node => {
      const dims = NODE_DIMENSIONS[node.type] || NODE_DIMENSIONS.default;
      return {
        id: node.id,
        width: dims.width,
        height: dims.height,
      };
    }),
    edges: visibleEdges.map(edge => ({
      id: edge.id,
      sources: [edge.source],
      targets: [edge.target],
    })),
  };

  // Run ELK layout
  const layoutResult = await elk.layout(elkGraph);

  // Map computed positions back to React Flow nodes
  const positionMap = {};
  for (const child of layoutResult.children || []) {
    positionMap[child.id] = {
      x: Math.round(child.x),
      y: Math.round(child.y),
    };
  }

  const layoutedNodes = nodes.map(node => {
    const pos = positionMap[node.id];
    if (pos) {
      return {
        ...node,
        position: pos,
      };
    }
    // Hidden nodes keep their position (they won't be rendered)
    return node;
  });

  return { nodes: layoutedNodes, edges };
}

/**
 * Re-layout after expand/collapse toggle.
 * Filters out hidden nodes, runs ELK, then returns updated nodes.
 */
export async function relayoutAfterToggle(nodes, edges, options = {}) {
  return computeElkLayout(nodes, edges, options);
}
