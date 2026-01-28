from pathlib import Path
from app.core.config import settings

class LocalStorage:
    def __init__(self):
        self.base_dir = Path(settings.RENDERS_DIR)
        self.base_dir.mkdir(exist_ok=True)
    
    def exists(self, render_id: str)-> bool:
        return self._path(render_id).exists()
    
    def save(self, temp_html_path: Path, render_id: str)-> Path:
        final_path = self._path(render_id)
        temp_html_path.replace(final_path)
        return final_path
    
    def public_url(self, render_id: str)-> str:
        return f"/renders/{render_id}.html"
    
    def _path(self, render_id: str)-> Path:
        return self.base_dir / f"{render_id}.html"

from pathlib import Path
from app.core.config import settings


class LocalStorage:
    """
    Storage abstraction.
    Today: local filesystem
    Tomorrow: S3 / R2
    
    """

    def __init__(self):
        self.base_dir = Path(settings.RENDERS_DIR)
        self.base_dir.mkdir(exist_ok=True)

    def exists(self, render_id: str) -> bool:
        return self._path(render_id).exists()

    def save(self, temp_html_path: Path, render_id: str) -> Path:
        final_path = self._path(render_id)
        temp_html_path.replace(final_path)
        return final_path

    def public_url(self, render_id: str) -> str:
        return f"/renders/{render_id}.html"

    def _path(self, render_id: str) -> Path:
        return self.base_dir / f"{render_id}.html"
