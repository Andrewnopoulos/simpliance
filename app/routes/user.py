import uuid

from fastapi import APIRouter

from data.datastore import Storage
from data.models import User

user_router = APIRouter(prefix='/users',
                        tags=['users'])

@user_router.get("/")
def read_users():
    with Storage() as s:
        all_users = s.get_all(User)
    return [u.dict() for u in all_users]

@user_router.post("/{name}")
def create_user(name: str):
    with Storage() as s:
        new_user = User(str(uuid.uuid4()), name)
        s.insert(new_user)

        return new_user.dict()
