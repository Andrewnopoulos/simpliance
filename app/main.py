import os

from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from worker import Worker

task_states = {}
worker = Worker(task_states)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Do setup
    worker.daemon = True
    worker.start()
    yield
    ## Do cleanup
    worker.put("quit")
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
    return worker.put("My_info")

@app.get("/reports")
def get_all_reports():
    return task_states

@app.get("/reports/{task_id}")
def get_report(task_id: str):
    if task_id in task_states:
        if task_states[task_id] == "done":
            filename = os.path.join("/results", f"{task_id}.html")
            try:
                with open(filename, 'r') as f:
                    html_content = f.read()
                return HTMLResponse(content=html_content, status_code=200)
            except:
                return JSONResponse({"error": f"Failed to find {filename}"})
        return {"state": task_states[task_id]}
    else:
        return HTMLResponse(None, status_code=404)