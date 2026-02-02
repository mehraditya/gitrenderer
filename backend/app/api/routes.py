import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.models.schemas import (
    RenderRequest,
    RenderResponse,
    RenderStatusResponse,)
from app.services.renderer import render_repository
from services.storage import LocalStorage
from sqlalchemy.org import Session
from app.api.deps import get_db
from app.models.job import Job


router = APIRouter()

@router.post("/render", response_model = RenderResponse)

async def start_render(
        payload: RenderRequest,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
):
    job_id = uuid.uuid4().hex

    job = Job(
        job_id = job_id,
        repo_url = payload.repo_url,
        status = "queued",
    )
    db.add(job)
    db.commit()
    
    background_tasks.add_task(_run_render_job, job_id)

    return RenderResponse(job_id=job_id, status="queued")

@router.get("/render/{job_id}", response_model = RenderStatusResponse)

async def get_render_status(job_id: str, db: Session = Depends(get_db),):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code =404, detail = "Job not found")

    storage = LocalStorage()

    return RenderStatusResponse(
        job_id=job_id,
        status = job.status,
        url = storage.public_url(job.render_id) if job.render_id else None,
        error = job.error,
    )

async def _run_render_job(job_id: str):
    from app.core.db import SessionLocal

    db = SessionLocal()
    try:
        job = db.get(Job, job_id)
        job.status = "running"
        db.commit()

        render_id = await render_repository(job.repo_url)

        job.status = "ready"
        job.render_id = render_id
        db.commit()
    
    except Exception as exc:
        job.status = "failed"
        job.error = str(exc)
        db.commit()

    finally:
        db.close()


    