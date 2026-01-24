from fastapi import APIRouter, HTTPException
from app.models import RenderRequest, RenderResponse
from app.renderer import render_repository

router = APIRouter()

@router.post("/render", response_model = RenderResponse)
def render_repo(payload: RenderRequest):
    try:
        render_id = render_repository(payload.repo_url)
    except Exception as exc:
        raise HTTPException(status_code = 500, detail = str(exc))
    return RenderResponse (
        status = "ready",
        repo_url = payload.repo_url,
        render_id = render_id,
        url = f"/renders/{render_id}.html",
    )
