from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles 
from app.api.routes import router
from app.models.job import Base
from app.core.db import engine

app = FastAPI(
    title = "Rendergit Web",
    version = "0.1.0",
)
Base.metadata.create_all(bind=engine)

app.include_routers(router)

app.mount("/renders",
        StaticFiles(directory = "renders"),
        name = "renders",
)

