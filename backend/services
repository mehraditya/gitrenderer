import hashlib
import subprocess
import tempfile
from pathlib import Path

RENDERS_DIR = Path("renders")
RENDERS_DIR.mkdir(exist_ok=True)

def _render_id(repo_url: str)-> str:
    return hashlib.sha256(repo_url.encode()).hexdigest()

def _directory_size_bytes(path: Path)-> int:
    total = 0
    for file in path.rglob("*"):
        if file.is_file():
            total += file.stat().st_size
    return total

def _file_count(path: Path)-> int:
    return sum(1 for p in path.rglob("*") if p.is_file())




def render_repository(repo_url: str)-> str:
    render_id = _render_id(repo_url)
    output_path = RENDERS_DIR/f"{render_id}.html"
    if output_path.exists():
        return render_id 
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(
            ["rendergit", repo_url],
            cwd = tmpdir,
            check = True,
            stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL,
            timeout= 60,
        )
        tmp_path = Path(tmpdir)
        size_mb = _directory_size_bytes(tmp_path) / (1024*1024) 
        if size_mb > MAX_REPO_SIZE_MB:
            raise RuntimeError(f"Repository too large: {size_mb: .2f} MB")

        if _file_count(tmp_path) > MAX_FILE_COUNT:
            raise RuntimeError("Repository has too many files")

        html_files = list(Path(tmpdir).glob("*.html"))
        if not html_files:
            raise RuntimeError("rendergit did not produce any html output")
            
        html_files[0].replace(output_path)
        
        return render_id                  