from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.mindmap_service import generate_mindmap

router = APIRouter(tags=["Mindmap Generation"])

class MindmapRequest(BaseModel):
    session_id: str

@router.post("/mindmap/generate", summary="Generate Mindmap")
def generate_mindmap_api(req: MindmapRequest):
    mermaid_text, png_path, svg_path, msg = generate_mindmap(req.session_id)

    if mermaid_text is None:
        return {
            "success": False,
            "message": msg,
            "mermaid_text": None,
            "png_url": None,
            "svg_url": None
        }

    # Convert file paths to URLs
    png_url = None
    svg_url = None

    if png_path:
        # Extract just the filename from the path
        import os
        png_filename = os.path.basename(png_path)
        png_url = f"/static/mindmaps/{png_filename}"

    if svg_path:
        # Extract just the filename from the path
        import os
        svg_filename = os.path.basename(svg_path)
        svg_url = f"/static/mindmaps/{svg_filename}"

    return {
        "success": True,
        "message": msg,
        "mermaid_text": mermaid_text,
        "png_url": png_url,
        "svg_url": svg_url
    }
