import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.schema import (
    RenderRequest,
    RenderResponse,
    RenderStatusResponse,)
from app.services.renderer import render_repository
from services.storage import LocalStorage

router = APIRouter()

_JOBS: dict[str, dict] = {}@router.post("/render", response_model = RenderResponse)

async def start_render(
        payload: RenderRequest,
        background_tasks: BackgroundTasks
):
    job_id = uuid.uuid4().hex

    _JOBS[job_id] = {"status":"queued", "url": None, "error":None,
                     }
    
    background_tasks.add_task(_run_render_job, job_id, payload.repo_url)

    return RenderResponse(job_id=job_id, status="queued",)

@router.get("/render/{job_id}", response_model = RenderStatusResponse)

async def get_render_status(job_id: str):
    job = _JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code =404, detail = "Job not found")
    return RenderStatusResponse(
        job_id=job_id,
        status = job["status"],
        url = job["url"],
        error = job["error"],
    )

async def _run_render_job(job_id:str, repo_url: str):
    try:
        _JOBS[job_id]["status"] = "running"
    
        render_id = await render_repository(repo_url)
        storage = LocalStorage()

        _JOBS[job_id]["status"] = "ready"
        _JOBS[job_id]["url"] = storage.public_url(render_id)
    except Exception as exc:
        _JOBS[job_id]["status"] = "failed"
        _JOBS[job_id]["error"] = str(exc)


    