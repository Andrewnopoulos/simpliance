import os
from datetime import datetime as dt
from datetime import timedelta as td

import pendulum

from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from data.models import Report, User, AuthKeys
from worker import Worker2
from data.datastore import Storage, create_schema

from settings import RESULTS_PATH, DB_PATH

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="test/token")

test_router = APIRouter(prefix='/test',
                          tags=['test'])

def get_user_from_token(token):
    with Storage() as s:
        user = s.get_one(User, {'name': token})
    return user or None

def fake_decode_token(token):
    return get_user_from_token(token)

def fake_hash_function(password):
    return "hash_" + password

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user

# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# @test_router.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

#     with Storage() as s:
#         user = s.get_one(User, {'email': form_data.username})

#     if not user:
#         raise HTTPException(status_code=400, detail="Email not found")

#     hashed_password = fake_hash_function(form_data.password)
#     print(hashed_password)
#     print(user.hashed_password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     return {"access_token": user.name, "token_type": "bearer"}

# @test_router.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user

# @test_router.get("/get_token/")
# async def read_token(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

# @test_router.get("/landing", response_class=HTMLResponse)
# def read_landing():
#     with open("content/new.html", 'r') as f:
#         html_content = f.read()
#     return HTMLResponse(content=html_content, status_code=200)

# @test_router.post("/reset_test_env/{user_name}")
# def reset_test_env(user_name: str, keys: AuthKeys):
#     os.remove(DB_PATH)

#     create_schema()

#     u = User(str(uuid.uuid4()), user_name, 'test_email')
#     u.hashed_password = 'hash_hello'
#     with Storage() as s:
#         s.insert(u)
#         keys.id = str(uuid.uuid4())
#         keys.user_id = u.id
#         s.insert(keys)

#     return (u, keys)

def generate_report(s: Storage, user_id: str, status: str):
    r = Report(str(uuid.uuid4()),
               status,
               pendulum.now().to_iso8601_string(),
               pendulum.now().add(minutes=4).to_iso8601_string(), "test benchmark", user_id, str(uuid.uuid4()))
    s.insert(r)

@test_router.get("/populate/{user_id}")
def populate_reports(user_id: str):
    with Storage() as s:
        generate_report(s, user_id, "queued")
        generate_report(s, user_id, "progress")
        generate_report(s, user_id, "done")
        generate_report(s, user_id, "queued")
        generate_report(s, user_id, "progress")
        generate_report(s, user_id, "done")

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