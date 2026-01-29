import asyncio
import hashlib
import tempfile
from pathlib import Path

from app.core.config import settings
from app.services.storage import LocalStorage


def _render_id(repo_url: str) -> str:
    return hashlib.sha256(repo_url.encode()).hexdigest()


def _directory_size_bytes(path: Path) -> int:
    total = 0
    for file in path.rglob("*"):
        if file.is_file():
            total += file.stat().st_size
    return total


def _file_count(path: Path) -> int:
    return sum(1 for p in path.rglob("*") if p.is_file())


async def render_repository(repo_url: str) -> str:
    render_id = _render_id(repo_url)
    storage = LocalStorage()

    if storage.exists(render_id):
        return render_id

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        process = await asyncio.create_subprocess_exec(
            "rendergit",
            repo_url,
            cwd=tmp_path,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            await asyncio.wait_for(
                process.communicate(),
                timeout=settings.RENDER_TIMEOUT,
            )
        except asyncio.TimeoutError:
            process.kill()
            raise RuntimeError("Rendering timed out")

        if process.returncode != 0:
            raise RuntimeError("rendergit execution failed")

        size_mb = _directory_size_bytes(tmp_path) / (1024 * 1024)
        if size_mb > settings.MAX_REPO_SIZE_MB:
            raise RuntimeError(f"Repository too large: {size_mb:.2f} MB")

        if _file_count(tmp_path) > settings.MAX_FILE_COUNT:
            raise RuntimeError("Repository has too many files")

        html_files = list(tmp_path.glob("*.html"))
        if not html_files:
            raise RuntimeError("rendergit did not produce HTML output")

        storage.save(html_files[0], render_id)

    return render_id
