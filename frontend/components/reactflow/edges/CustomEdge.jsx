/**
 * CustomEdge — Premium edges with gradient strokes and smooth curves.
 * Uses React Flow's getBezierPath to eliminate SVG errors.
 *
 * Levels:
 *   primary   → course → week  (thicker, indigo gradient)
 *   secondary → week → day     (thinner, teal, dashed)
 */
import React, { useId } from 'react';
import { getBezierPath } from 'reactflow';

const CustomEdge = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  markerEnd,
  data,
}) => {
  const level = data?.level || 'primary';
  const gradientId = `edge-gradient-${id}`;

  // Use React Flow's built-in path — zero NaN errors
  const [edgePath] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
    curvature: 0.4,
  });

  const isPrimary = level === 'primary';

  return (
    <>
      {/* Gradient definition */}
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
          {isPrimary ? (
            <>
              <stop offset="0%" stopColor="#a5b4fc" stopOpacity="0.6" />
              <stop offset="50%" stopColor="#818cf8" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#6366f1" stopOpacity="0.7" />
            </>
          ) : (
            <>
              <stop offset="0%" stopColor="#6ee7b7" stopOpacity="0.4" />
              <stop offset="50%" stopColor="#34d399" stopOpacity="0.65" />
              <stop offset="100%" stopColor="#10b981" stopOpacity="0.5" />
            </>
          )}
        </linearGradient>
      </defs>

      {/* Invisible wider hit-area */}
      <path
        d={edgePath}
        fill="none"
        stroke="transparent"
        strokeWidth={24}
        className="react-flow__edge-interaction"
      />

      {/* Soft glow behind edge */}
      <path
        d={edgePath}
        fill="none"
        stroke={isPrimary ? '#818cf8' : '#34d399'}
        strokeWidth={isPrimary ? 7 : 5}
        strokeOpacity={0.06}
        strokeLinecap="round"
        style={{ filter: 'blur(5px)' }}
      />

      {/* Visible edge with gradient */}
      <path
        id={id}
        className="react-flow__edge-path"
        d={edgePath}
        fill="none"
        stroke={`url(#${gradientId})`}
        strokeWidth={isPrimary ? 2.5 : 1.8}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={isPrimary ? 'none' : '6 4'}
        style={isPrimary ? undefined : {
          animation: 'edgeFlow 2s linear infinite',
        }}
        markerEnd={markerEnd}
      />
    </>
  );
};

export default CustomEdge;