import os
import subprocess
from typing import Dict, Any

from app.utils.session_store import session_store

# Correct folder constant
MINDMAP_DIR = os.path.join("app", "static", "mindmaps")


def generate_mermaid_text(course: Dict[str, Any]) -> str:
    """
    Generate professional-looking Mermaid mindmap with correct syntax
    """
    lines = []

    # Add theme configuration for better styling
    lines.append('%%{init: {"theme": "base", "themeVariables": {')
    lines.append('    "primaryColor": "#2563eb",')
    lines.append('    "primaryBorderColor": "#1d4ed8",')
    lines.append('    "lineColor": "#6b7280",')
    lines.append('    "fontSize": "18px",')
    lines.append('    "fontFamily": "Inter, sans-serif",')
    lines.append('    "secondaryColor": "#f1f5f9",')
    lines.append('    "tertiaryColor": "#1e293b",')
    lines.append('    "primaryTextColor": "#ffffff",')
    lines.append('    "secondaryTextColor": "#64748b"')
    lines.append('}}}%%')

    # Use TB (top to bottom) layout for better vertical flow
    lines.append("graph TB")

    course_title = course.get("title", "Course")
    course_node = "COURSE"

    # Add course title with styling
    lines.append(f'    {course_node}["{course_title}"]')
    lines.append(f'    classDef courseNode fill:#2563eb,color:#ffffff,stroke:#1d4ed8,stroke-width:3px,rx:10,ry:10')

    week_counter = 1
    week_nodes = []

    for week in course.get("weeks", []):
        week_id = f"W{week_counter}"
        week_title = week.get("title", f"Week {week_counter}")
        lines.append(f'    {course_node} --> {week_id}["Week {week_counter}<br/>{week_title}"]')
        week_nodes.append(week_id)

        day_counter = 1
        for day in week.get("days", []):
            day_id = f"{week_id}D{day_counter}"
            day_title = day.get("title", f"Day {day_counter}")
            lines.append(f'    {week_id} --> {day_id}["Day {day_counter}<br/>{day_title}"]')
            day_counter += 1

        week_counter += 1

    # Add styling for different node types
    lines.append("")
    lines.append("    classDef weekNode fill:#059669,color:#ffffff,stroke:#047857,stroke-width:2px,rx:8,ry:8")
    lines.append("    classDef dayNode fill:#d97706,color:#ffffff,stroke:#b45307,stroke-width:1px,rx:6,ry:6")
    lines.append("")
    lines.append("    class COURSE courseNode")

    # Apply week and day styling
    if week_nodes:
        lines.append(f"    class {','.join(week_nodes)} weekNode;")

    # Add some spacing and layout improvements
    lines.append("")
    lines.append("    %% Layout improvements")
    lines.append("    linkStyle 0 stroke:#6b7280,stroke-width:2px,curve:spline")

    return "\n".join(lines)


def save_mermaid_file(content: str, session_id: str) -> str:
    os.makedirs(MINDMAP_DIR, exist_ok=True)

    file_path = os.path.join(MINDMAP_DIR, f"{session_id}.mmd")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def render_mermaid_images(mmd_path: str, session_id: str) -> tuple:
    """
    Render both PNG and SVG images using mmdc (Mermaid CLI)
    Returns (png_path, svg_path) or fallback placeholder if failed
    """
    try:
        # Ensure directory exists
        os.makedirs(MINDMAP_DIR, exist_ok=True)

        # Generate output file paths
        png_path = os.path.join(MINDMAP_DIR, f"{session_id}.png")
        svg_path = os.path.join(MINDMAP_DIR, f"{session_id}.svg")

        # Try to render SVG
        svg_cmd = ["npx", "@mermaid-js/mermaid-cli", "-i", mmd_path, "-o", svg_path]
        svg_success = False
        try:
            result_svg = subprocess.run(svg_cmd, capture_output=True, text=True, timeout=30)
            if result_svg.returncode == 0 and os.path.exists(svg_path):
                print(f"SVG rendered successfully: {svg_path}")
                svg_success = True
            else:
                print(f"SVG rendering failed: {result_svg.stderr}")
        except subprocess.TimeoutExpired:
            print("SVG rendering timed out")
        except Exception as e:
            print(f"SVG rendering error: {e}")

        # Try to render PNG
        png_cmd = ["npx", "@mermaid-js/mermaid-cli", "-i", mmd_path, "-o", png_path]
        png_success = False
        try:
            result_png = subprocess.run(png_cmd, capture_output=True, text=True, timeout=30)
            if result_png.returncode == 0 and os.path.exists(png_path):
                print(f"PNG rendered successfully: {png_path}")
                png_success = True
            else:
                print(f"PNG rendering failed: {result_png.stderr}")
        except subprocess.TimeoutExpired:
            print("PNG rendering timed out")
        except Exception as e:
            print(f"PNG rendering error: {e}")

        # If both failed, create placeholder SVG
        if not svg_success and not png_success:
            print("Both rendering failed, creating placeholder SVG")
            svg_path = create_placeholder_svg(mmd_path, session_id)
            return None, svg_path

        # Return paths (None if failed)
        final_png_path = png_path if png_success else None
        final_svg_path = svg_path if svg_success else None

        return final_png_path, final_svg_path

    except Exception as e:
        print(f"Error in render_mermaid_images: {e}")
        # Fallback to placeholder
        try:
            svg_path = create_placeholder_svg(mmd_path, session_id)
            return None, svg_path
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            return None, None


def create_placeholder_svg(mmd_path: str, session_id: str) -> str:
    """
    Create a placeholder SVG when Mermaid CLI fails
    """
    try:
        svg_path = os.path.join(MINDMAP_DIR, f"{session_id}.svg")

        # Create a simple placeholder SVG
        placeholder_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .bg {{ fill: #f8fafc; }}
      .header {{ fill: #1e293b; font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; }}
      .subheader {{ fill: #64748b; font-family: Arial, sans-serif; font-size: 16px; }}
      .content {{ fill: #334155; font-family: Arial, sans-serif; font-size: 14px; }}
      .accent {{ fill: #3b82f6; }}
      .button {{ fill: #ef4444; rx: 8; ry: 8; }}
      .button-text {{ fill: white; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="800" height="600" class="bg"/>

  <!-- Header -->
  <text x="400" y="80" text-anchor="middle" class="header">Course Mindmap</text>
  <text x="400" y="110" text-anchor="middle" class="subheader">Generated with CourseCraft-AI</text>

  <!-- Mermaid Code Display -->
  <rect x="50" y="150" width="700" height="300" fill="white" rx="12" ry="12" stroke="#e2e8f0" stroke-width="2"/>

  <text x="80" y="180" class="content">Generated Mermaid Code:</text>

  <foreignObject x="80" y="190" width="640" height="250">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: monospace; font-size: 12px; color: #1e293b; white-space: pre; overflow: auto; height: 100%;">
      graph TB<br/>    COURSE["Advanced String: Expert Level Training"]<br/>    COURSE --> W1["Week 1: Core Concepts"]<br/>    W1 --> W1D1["Day 1: Fundamentals"]<br/>    W1 --> W1D2["Day 2: Fundamentals"]<br/>    W1 --> W1D3["Day 3: Fundamentals"]<br/>    W1 --> W1D4["Day 4: Fundamentals"]<br/>    W1 --> W1D5["Day 5: Fundamentals"]<br/>    COURSE --> W2["Week 2: Core Concepts"]<br/>    W2 --> W2D1["Day 1: Fundamentals"]<br/>    ... (truncated for display)
    </div>
  </foreignObject>

  <!-- Instructions -->
  <text x="400" y="480" text-anchor="middle" class="content">
    Note: Professional rendering requires Mermaid CLI
  </text>
  <text x="400" y="500" text-anchor="middle" class="content">
    Install with: npm install -g @mermaid-js/mermaid-cli
  </text>

  <!-- Download Button -->
  <rect x="300" y="530" width="200" height="40" class="button"/>
  <text x="400" y="555" text-anchor="middle" class="button-text">Download Mermaid Code</text>
</svg>'''

        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(placeholder_content)

        print(f"Placeholder SVG created at {svg_path}")
        return svg_path

    except Exception as e:
        print(f"Failed to create placeholder SVG: {str(e)}")
        return None


def generate_mindmap(session_id: str):
    session = session_store.get_session(session_id)

    if not session:
        return None, None, None, "Session not found"

    course = session.get("course")
    if not course:
        return None, None, None, "Course data missing"

    # Step 1: Create improved Mermaid text with professional styling
    mermaid_text = generate_mermaid_text(course)

    # Step 2: Save .mmd file
    mmd_path = save_mermaid_file(mermaid_text, session_id)

    # Step 3: Render both PNG and SVG
    png_path, svg_path = render_mermaid_images(mmd_path, session_id)

    if not png_path and not svg_path:
        return mermaid_text, None, None, "Failed to render both PNG and SVG"

    return mermaid_text, png_path, svg_path, "success"