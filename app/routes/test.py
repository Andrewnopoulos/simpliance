import os

from typing import Union
import uuid
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from data.models import Report, User
from worker import Worker2
from data.datastore import Storage

from settings import RESULTS_PATH

test_router = APIRouter(prefix='/test',
                          tags=['test'])

@test_router.get("/landing", response_class=HTMLResponse)
def read_landing():
    with open("content/new.html", 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@test_router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@test_router.get("/generate")
def generate_report():
    new_user = User(str(uuid.uuid4()), "Andrew")
    with Storage() as s:
        s.insert(new_user)
    return Worker2().put(new_user, "test_benchmark")

@test_router.get("/reports")
def get_all_reports():
    with Storage() as s:
        return [r.dict() for r in s.get_all(Report)]

@test_router.get("/reports/{task_id}")
def get_report(task_id: str):
    with Storage() as s:
        task = s.get_one(Report, {'id': task_id})
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