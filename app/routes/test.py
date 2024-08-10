import os

from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from data.models import Report, User, AuthKeys
from worker import Worker2
from data.datastore import Storage, create_schema

from settings import RESULTS_PATH, DB_PATH

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

test_router = APIRouter(prefix='/test',
                          tags=['test'])


def fake_decode_token(token):
    return User("fakedecoded_" + token, "test_user")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@test_router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@test_router.get("/get_token/")
async def read_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@test_router.get("/landing", response_class=HTMLResponse)
def read_landing():
    with open("content/new.html", 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@test_router.post("/reset_test_env/{user_name}")
def reset_test_env(user_name: str, keys: AuthKeys):
    os.remove(DB_PATH)

    create_schema()

    u = User(str(uuid.uuid4()), user_name)
    with Storage() as s:
        s.insert(u)
        keys.id = str(uuid.uuid4())
        keys.user_id = u.id
        s.insert(keys)

    return (u, keys)

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