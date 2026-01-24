from pydantic import BaseModel, HttpUrl

class RenderRequest(BaseModel):
    status: str
    repo_url: HttpUrl
    render_id: str
    url: str