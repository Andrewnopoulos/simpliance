import uuid

from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse

from data.datastore import Storage
from data.models import User
from pydantic import BaseModel

from .auth import get_password_hash, get_current_active_user

user_router = APIRouter(prefix='/users',
                        tags=['users'])

# POST /api/users - Create a new user
# GET /api/users/{id} - Get user details
# PUT /api/users/{id} - Update user details
# DELETE /api/users/{id} - Delete a user

class UserRegistration(BaseModel):
    email: str
    password: str

@user_router.post("/register")
async def register_user(registration_information: UserRegistration):
    name = "Please enter your name"
    email = registration_information.email
    password = registration_information.password
    u = User(str(uuid.uuid4()), name, email)
    u.hashed_password = get_password_hash(password)
    with Storage() as s:
        s.insert(u)

    return u

@user_router.get("/{id}")
async def get_user(id: str):
    with Storage() as s:
        desired_user = s.get_one(User, {'id': id})
    
    if not desired_user:
        raise HTTPException(status_code=404)

    return desired_user

class UserModification(BaseModel):
    name: str
    email: str

@user_router.put("/")
async def modify_user(user_data: UserModification, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        print(current_user)
        current_user.name = user_data.name
        current_user.email = user_data.email
        updated = s.update(current_user)

    return {'updated_users': updated}

@user_router.delete("/{id}")
async def delete_user(id: str):
    with Storage() as s:
        found_user: User = s.get_one(User, {'id': id})
        if not found_user:
            raise HTTPException(status_code=404)
        deleted = s.delete(found_user)

    return {'deleted_users': deleted}

@user_router.delete("/")
async def delete_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        deleted = s.delete(current_user)

    return {'deleted_users': deleted}
