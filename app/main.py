from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from database import crear_db
from controllers.hospital import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    crear_db()

    yield


app = FastAPI(
    lifespan=lifespan
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(router)