from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from worker import Worker2
from data.datastore import create_schema

from routes import (
    authkeys_router,
    user_router,
    report_router,
    interface_router,
    test_router,
    secure_router
)

from settings import DB_PATH

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_schema(DB_PATH)
    worker = Worker2()
    worker.db_path = DB_PATH
    ## Do setup
    worker.start_thread()
    yield
    ## Do cleanup
    worker.stop_thread()

app = FastAPI(lifespan=lifespan)

app.mount("/", StaticFiles(directory="public", html=True), name="static")

main_router = APIRouter(prefix='/api')

main_router.include_router(authkeys_router)
main_router.include_router(report_router)
main_router.include_router(user_router)
main_router.include_router(test_router)
main_router.include_router(secure_router)
main_router.include_router(interface_router)

app.include_router(main_router)

# Simply the root will return our Svelte build
@app.get("/", response_class=FileResponse)
async def main():
    return "public/index.html"
