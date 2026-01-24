from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles 
from app.api import router

app = FastAPI(
    title = "Rendergit Web",
    version = "0.1.0",
)
app.include_routers(router)
app.mount("/renders",
        StaticFiles(directory = "renders"),
        name = "renders",
)

