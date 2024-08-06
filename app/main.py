import os
import uuid

from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from worker import Worker
from data.datastore import create_schema, Storage
from data.models import Report, User, AuthKeys

DB_PATH = os.environ["DB_PATH"]
RESULTS_PATH = os.environ["RESULTS_PATH"]

storage = Storage(DB_PATH)
worker = Worker(storage)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Do setup
    create_schema(DB_PATH)
    worker.daemon = True
    worker.start()
    yield
    ## Do cleanup
    worker.exit()
    worker.join()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def read_root():
    return {"TEST": "THING"}

@app.get("/landing", response_class=HTMLResponse)
def read_landing():
    with open("content/new.html", 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/generate")
def generate_report():
    new_user = User(str(uuid.uuid4()), "Andrew")
    storage.insert(new_user)
    return worker.put(new_user, "test_benchmark")

@app.get("/reports")
def get_all_reports():
    return [r.dict() for r in storage.get_all(Report)]

@app.get("/reports/{task_id}")
def get_report(task_id: str):
    task = storage.get_one(Report, {'id': task_id})
    if not task:
        return HTMLResponse(None, status_code=404)
    if task.process_state == "done":
        filename = os.path.join(RESULTS_PATH, f"{task_id}.html")
        print(f"searching for {filename}")
        try:
            with open(filename, 'r') as f:
                html_content = f.read()
            return HTMLResponse(content=html_content, status_code=200)
        except:
            return JSONResponse({"error": f"Failed to find {filename}"})
    else:
        return task