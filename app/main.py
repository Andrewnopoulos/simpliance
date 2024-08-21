from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from worker import Worker2
from data.datastore import create_schema

from routes import (
    authkeys_router,
    user_router,
    report_router,
    auth_router
)

from test_routes import (
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://localhost:5173",
                   "http://localhost:4173",
                   "http://127.0.0.1:3000",
                   "http://127.0.0.1:5173",
                   "http://127.0.0.1:4173",
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_router = APIRouter(prefix='/api')

main_router.include_router(authkeys_router)
main_router.include_router(report_router)
main_router.include_router(user_router)
main_router.include_router(auth_router)

debug_router = APIRouter(prefix='/debug')

debug_router.include_router(test_router)
debug_router.include_router(secure_router)
debug_router.include_router(interface_router)

app.include_router(main_router)
app.include_router(debug_router)