from pydantic import BaseModel, HttpUrl

class RenderRequest(BaseModel):
    repo_url: HttpUrl


class RenderResponse(BaseModel):
    job_id: str
    status: str


class RenderStatusResponse(BaseModel):
    job_id: str
    status: str
    url: str | None = None
    error: str | None = None
