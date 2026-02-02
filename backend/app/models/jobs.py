from datetime import datetime
from sqlalchemy import String, DateTime 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Job(Base):
    __tablename__ = "jobs"

    job_id: Mapped[str] = mapped_column(String, primary_key = True)
    repo_url: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    render_id: Mapped[str |None]