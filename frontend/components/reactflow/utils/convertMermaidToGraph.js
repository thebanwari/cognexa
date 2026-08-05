/**
 * Mermaid Text → React Flow Graph Converter
 *
 * Parses Mermaid flowchart syntax and produces React Flow nodes and edges.
 * Positions are NOT computed here — they are set to (0,0) and computed by ELK.
 */

/* ── helpers ───────────────────────────────────────────────────── */

function stripHtml(raw) {
  if (!raw || typeof raw !== 'string') return raw || '';
  return raw
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<\/?[^>]+(>|$)/g, '')
    .trim();
}

/**
 * Strips redundant prefixes like "Week 1:", "Day 2:" from titles
 * so nodes can show the prefix as a label and the rest as the title.
 * "Week 1: Core Concepts" → "Core Concepts"
 * "Day 3: Functions"      → "Functions"
 * "Advanced Topics"       → "Advanced Topics" (no prefix to strip)
 */
function cleanTitle(raw) {
  if (!raw || typeof raw !== 'string') return raw || '';
  return raw
    .replace(/^(Week|Day)\s*\d+\s*[:–—-]\s*/i, '')
    .trim() || raw;
}

/* ── main parser ───────────────────────────────────────────────── */

export function convertMermaidToGraph(mermaidText = '') {
  if (!mermaidText || typeof mermaidText !== 'string') {
    return { nodes: [], edges: [] };
  }

  // Clean input
  const cleaned = mermaidText
    .replace(/%%\{[\s\S]*?\}%%/g, '')        // remove init blocks
    .split('\n')
    .map(l => l.trim())
    .filter(l => {
      if (!l) return false;
      const skip = [
        'classDef', 'class ', 'style ', 'linkStyle',
        '%%', 'click ', 'flowchart', 'sequenceDiagram',
      ];
      return !skip.some(s => l.startsWith(s));
    });

  // ── Extract labels and connections ─────────────────────────────
  const labels = {};
  const connections = [];

  const nodePattern = /^([A-Za-z0-9_]+)\s*\[\s*"([^"]*)"\s*\]/;
  const arrowPattern = /([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)/g;
  const arrowWithNodePattern = /-->\s*([A-Za-z0-9_]+)\s*\[\s*"([^"]*)"\s*\]/g;

  for (const line of cleaned) {
    // Extract standalone node labels
    const nm = line.match(nodePattern);
    if (nm) {
      labels[nm[1].trim()] = nm[2].trim();
    }

    // Extract labels defined inline with arrows
    arrowWithNodePattern.lastIndex = 0;
    let nodeMatch;
    while ((nodeMatch = arrowWithNodePattern.exec(line)) !== null) {
      const id = nodeMatch[1].trim();
      const rawLabel = nodeMatch[2].trim();
      if (id && rawLabel) labels[id] = rawLabel;
    }

    // Extract connections
    arrowPattern.lastIndex = 0;
    let m;
    while ((m = arrowPattern.exec(line)) !== null) {
      const source = m[1].trim();
      const target = m[2].trim();
      if (source && target) connections.push({ source, target });
    }
  }

  // ── Classify nodes ────────────────────────────────────────────
  const nodeIds = Object.keys(labels);
  const courseId =
    nodeIds.find(id => id.toUpperCase() === 'COURSE') || nodeIds[0] || null;

  if (!courseId) return { nodes: [], edges: [] };

  const weekRegex = /^W(\d+)$/i;
  const dayRegex = /^W(\d+)D(\d+)$/i;

  const weeks = [];
  const days = [];

  for (const id of nodeIds) {
    if (id === courseId) continue;

    const wk = id.match(weekRegex);
    const dy = id.match(dayRegex);

    if (dy) {
      days.push({
        id,
        weekNumber: Number(dy[1]),
        number: Number(dy[2]),
        rawLabel: labels[id] || id,
      });
    } else if (wk) {
      weeks.push({
        id,
        number: Number(wk[1]),
        rawLabel: labels[id] || id,
      });
    } else {
      // Treat unknown nodes as weeks
      weeks.push({
        id,
        number: weeks.length + 1,
        rawLabel: labels[id] || id,
      });
    }
  }

  weeks.sort((a, b) => a.number - b.number);
  days.sort((a, b) => a.weekNumber - b.weekNumber || a.number - b.number);

  // ── Build React Flow nodes (positions = 0,0 — ELK will compute) ──

  const courseLabel = labels[courseId] || 'Course';
  const courseNode = {
    id: courseId,
    type: 'courseNode',
    position: { x: 0, y: 0 },
    data: {
      id: courseId,
      title: stripHtml(courseLabel),
      rawLabel: courseLabel,
      nodeType: 'course',
      description: stripHtml(courseLabel),
      metadata: { weeks: weeks.length, totalDays: days.length },
    },
  };

  const weekNodes = weeks.map(w => {
    const rawLabel = w.rawLabel || `Week ${w.number}`;
    const relatedDays = days.filter(d => d.weekNumber === w.number);
    return {
      id: w.id,
      type: 'weekNode',
      position: { x: 0, y: 0 },
      data: {
        id: w.id,
        title: cleanTitle(stripHtml(rawLabel)),
        rawLabel,
        nodeType: 'week',
        number: w.number,
        isCollapsed: true,
        relatedDays: relatedDays.map(d => d.id),
        description: stripHtml(rawLabel),
        metadata: {
          days: relatedDays.length,
          weekNumber: w.number,
        },
      },
    };
  });

  const dayNodes = days.map(d => {
    const rawLabel = d.rawLabel || `Day ${d.number}`;
    const weekId = weeks.find(w => w.number === d.weekNumber)?.id || '';
    return {
      id: d.id,
      type: 'dayNode',
      position: { x: 0, y: 0 },
      hidden: true, // collapsed by default
      data: {
        id: d.id,
        title: cleanTitle(stripHtml(rawLabel)),
        rawLabel,
        nodeType: 'day',
        number: d.number,
        weekId,
        weekNumber: d.weekNumber,
        description: stripHtml(rawLabel),
        metadata: { weekId, weekNumber: d.weekNumber },
      },
    };
  });

  // ── Build edges ───────────────────────────────────────────────
  const edges = [];
  const edgeSet = new Set();

  function addEdge(source, target, level = 'primary') {
    const key = `${source}-->${target}`;
    if (edgeSet.has(key)) return;
    edgeSet.add(key);
    edges.push({
      id: `e_${source}_${target}`,
      source,
      target,
      type: 'customEdge',
      animated: false,
      data: { level },
    });
  }

  // Parsed connections
  for (const c of connections) addEdge(c.source, c.target);

  // Ensure course→week edges
  for (const wk of weekNodes) addEdge(courseNode.id, wk.id, 'primary');

  // Ensure week→day edges
  for (const dn of dayNodes) addEdge(dn.data.weekId, dn.id, 'secondary');

  const nodes = [courseNode, ...weekNodes, ...dayNodes];
  return { nodes, edges };
}

/* ── Expand / Collapse ──────────────────────────────────────────── */

export function toggleWeekExpansion(nodes = [], edges = [], weekId) {
  if (!weekId) return { nodes, edges };

  const updated = nodes.map(n => ({ ...n, data: { ...(n.data || {}) } }));
  const wkIdx = updated.findIndex(
    n => n.id === weekId && n.type === 'weekNode'
  );
  if (wkIdx === -1) return { nodes, edges };

  // Toggle
  updated[wkIdx].data.isCollapsed = !updated[wkIdx].data.isCollapsed;
  const isCollapsed = updated[wkIdx].data.isCollapsed;

  // Show/hide day nodes belonging to this week
  for (let i = 0; i < updated.length; i++) {
    if (
      updated[i].type === 'dayNode' &&
      updated[i].data?.weekId === weekId
    ) {
      updated[i] = { ...updated[i], hidden: isCollapsed };
    }
  }

  return { nodes: updated, edges };
}

/* ── Node detail extractor (for Sidebar) ────────────────────────── */

export function getNodeDetails(nodeId, nodes = []) {
  if (!nodeId) return null;
  const n = nodes.find(x => x.id === nodeId);
  if (!n) return null;

  const typeMap = {
    courseNode: 'course',
    weekNode: 'week',
    dayNode: 'day',
  };

  return {
    id: n.id,
    title: n.data?.title || n.data?.rawLabel || n.id,
    type: typeMap[n.type] || n.data?.nodeType || n.type,
    description: n.data?.description || '',
    metadata: n.data?.metadata || {},
  };
}
