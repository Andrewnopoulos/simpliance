import uuid

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from data.datastore import Storage
from data.models import User

user_router = APIRouter(prefix='/users',
                        tags=['users'])

@user_router.get("/")
def read_users():
    with Storage() as s:
        all_users = s.get_all(User)
    return [u.dict() for u in all_users]

@user_router.get("/{name}")
def get_user_by_name(name: str):
    with Storage() as s:
        desired_user = s.get_one(User, {'name': name})
    if not desired_user:
        return HTMLResponse(status_code=404)
    return desired_user

@user_router.post("/{name}")
def create_user(name: str):
    with Storage() as s:
        new_user = User(str(uuid.uuid4()), name, 'test_email')
        s.insert(new_user)

        return new_user.dict()
