import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

MINMAP_DIR = Path("static/mindmaps")


def create_placeholder_svg(session_id: str) -> str:
    """
    Create a placeholder SVG when Mermaid CLI fails
    """
    try:
        ensure_minmap_directory()
        output_svg = MINMAP_DIR / f"{session_id}.svg"

        # Create a simple placeholder SVG with the session info
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
  <text x="400" y="110" text-anchor="middle" class="subheader">Session: {session_id}</text>

  <!-- Mermaid Code Display -->
  <rect x="50" y="150" width="700" height="300" fill="white" rx="12" ry="12" stroke="#e2e8f0" stroke-width="2"/>

  <text x="80" y="180" class="content">Generated Mermaid Code:</text>

  <foreignObject x="80" y="190" width="640" height="250">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: monospace; font-size: 12px; color: #1e293b; white-space: pre; overflow: auto; height: 100%;">
      graph TB<br/>    COURSE["Introduction to String"]<br/>    COURSE --> W1["Week 1: Core Concepts"]<br/>    W1 --> W1D1["Day 1: Fundamentals"]<br/>    W1 --> W1D2["Day 2: Fundamentals"]<br/>    W1 --> W1D3["Day 3: Fundamentals"]<br/>    W1 --> W1D4["Day 4: Fundamentals"]<br/>    W1 --> W1D5["Day 5: Fundamentals"]<br/>    COURSE --> W2["Week 2: Core Concepts"]<br/>    W2 --> W2D1["Day 1: Fundamentals"]<br/>    ... (truncated for display)
    </div>
  </foreignObject>

  <!-- Instructions -->
  <text x="400" y="480" text-anchor="middle" class="content">
    Note: Mermaid CLI rendering is not available on this system
  </text>
  <text x="400" y="500" text-anchor="middle" class="content">
    Install with: npm install -g @mermaid-js/mermaid-cli
  </text>

  <!-- Download Button -->
  <rect x="300" y="530" width="200" height="40" class="button"/>
  <text x="400" y="555" text-anchor="middle" class="button-text">Download Mermaid Code</text>
</svg>'''

        with open(output_svg, 'w', encoding='utf-8') as f:
            f.write(placeholder_content)

        logger.info(f"Placeholder SVG created at {output_svg}")
        return str(output_svg)

    except Exception as e:
        logger.error(f"Failed to create placeholder SVG: {str(e)}")
        raise

def ensure_minmap_directory():
    """Ensure mindmap directory exists"""
    MINMAP_DIR.mkdir(parents=True, exist_ok=True)

def render_mermaid_hd(mmd_path: str, session_id: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Render Mermaid diagram to both HD PNG and SVG
    Returns tuple of (png_url, svg_url) relative paths
    """
    try:
        ensure_minmap_directory()

        # HD PNG configuration
        output_png = MINMAP_DIR / f"{session_id}.png"
        output_svg = MINMAP_DIR / f"{session_id}.svg"

        # Try Mermaid CLI rendering
        png_cmd = [
            "npx", "@mermaid-js/mermaid-cli",
            "-i", mmd_path,
            "-o", str(output_png),
            "--scale", "2",
            "--width", "2500",
            "--backgroundColor", "white",
            "--theme", "neutral",
            "--config", '{"themeVariables": {"primaryColor": "#3b82f6", "primaryTextColor": "#ffffff", "primaryBorderColor": "#1e40af", "lineColor": "#9ca3af", "secondaryColor": "#f3f4f6", "tertiaryColor": "#1f2937"}}'
        ]

        svg_cmd = [
            "npx", "@mermaid-js/mermaid-cli",
            "-i", mmd_path,
            "-o", str(output_svg),
            "--type", "svg",
            "--backgroundColor", "white",
            "--theme", "neutral",
            "--config", '{"themeVariables": {"primaryColor": "#3b82f6", "primaryTextColor": "#ffffff", "primaryBorderColor": "#1e40af", "lineColor": "#9ca3af", "secondaryColor": "#f3f4f6", "tertiaryColor": "#1f2937"}}'
        ]

        # Try multiple command variations for Windows compatibility
        commands_to_try = [
            (png_cmd, str(output_png), "PNG"),
            (svg_cmd, str(output_svg), "SVG")
        ]

        for cmd, output_file, file_type in commands_to_try:
            try:
                # Try with shell=True first (Windows)
                result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=30)

                if result.returncode != 0:
                    logger.warning(f"{file_type} rendering failed with shell=True: {result.stderr}")
                    # Try without shell=True
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    logger.info(f"{file_type} rendering completed for {session_id}")
                else:
                    logger.error(f"{file_type} rendering failed: {result.stderr}")

            except subprocess.TimeoutExpired:
                logger.error(f"{file_type} rendering timed out for {session_id}")
            except Exception as e:
                logger.error(f"Error rendering {file_type} for {session_id}: {str(e)}")

        # Check if files were created successfully
        png_url = None
        svg_url = None

        if output_png.exists() and output_png.stat().st_size > 0:
            png_url = f"/static/mindmaps/{session_id}.png"
            logger.info(f"PNG created successfully: {png_url}")

        if output_svg.exists() and output_svg.stat().st_size > 0:
            svg_url = f"/static/mindmaps/{session_id}.svg"
            logger.info(f"SVG created successfully: {svg_url}")

        # Fallback: Create a placeholder SVG if no files were generated
        if not png_url and not svg_url:
            logger.warning(f"No files generated, creating placeholder SVG for {session_id}")
            placeholder_svg = create_placeholder_svg(session_id)
            svg_url = f"/static/mindmaps/{session_id}.svg"
            logger.info(f"Placeholder SVG created: {svg_url}")

        return png_url, svg_url

    except Exception as e:
        logger.error(f"Error rendering mermaid for session {session_id}: {str(e)}")
        # Fallback to placeholder
        try:
            placeholder_svg = create_placeholder_svg(session_id)
            return None, f"/static/mindmaps/{session_id}.svg"
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {str(fallback_error)}")
            return None, None

def check_mermaid_cli():
    """Check if Mermaid CLI is available"""
    try:
        # Try multiple approaches for Windows compatibility
        commands_to_try = [
            ["npx", "@mermaid-js/mermaid-cli", "--version"],
            ["npm", "exec", "@mermaid-js/mermaid-cli", "--", "--version"],
            ["mermaid-cli", "--version"]
        ]

        for cmd in commands_to_try:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    shell=True  # Windows ke liye important
                )
                if result.returncode == 0:
                    logger.info(f"Mermaid CLI available via {cmd[0]}: {result.stdout.strip()}")
                    return True
            except Exception as e:
                logger.debug(f"Command {cmd} failed: {e}")
                continue

        logger.warning("Mermaid CLI not available through any method")
        return False
    except Exception as e:
        logger.error(f"Error checking Mermaid CLI: {e}")
        return False
    