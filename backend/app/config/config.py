from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MAX_REPO_SIZE_MB: int = 50
    MAX_FILE_COUNT: int = 1000
    RENDER_TIMEOUT: int = 60
    STORAGE_DIR: str = "renders"

settings = Settings()