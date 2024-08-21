import uuid

from typing import Annotated, Optional

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
    name: str
    email: str
    password: str

@user_router.post("/register")
async def register_user(registration_information: UserRegistration):
    name = registration_information.name
    email = registration_information.email
    password = registration_information.password
    u = User(str(uuid.uuid4()), name, email)
    u.hashed_password = get_password_hash(password)
    with Storage() as s:
        s.insert(u)

    return u

@user_router.get("/{id}")
async def get_user(id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        desired_user: User = s.get_one(User, {'id': id})
    
    if not desired_user:
        raise HTTPException(status_code=404)
    
    if desired_user.id == current_user.id:
        return desired_user
    
    return {'id': id}

class UserModification(BaseModel):
    name: Optional[str]
    email: Optional[str]

@user_router.put("/")
async def modify_user(user_data: UserModification, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        print(current_user)
        if user_data.name:
            current_user.name = user_data.name
        if user_data.email:
            current_user.email = user_data.email
        updated = s.update(current_user)

    return {'updated_users': updated}

# @user_router.delete("/{id}")
# async def delete_user(id: str):
#     with Storage() as s:
#         found_user: User = s.get_one(User, {'id': id})
#         if not found_user:
#             raise HTTPException(status_code=404)
#         deleted = s.delete(found_user)

#     return {'deleted_users': deleted}

@user_router.put("/{id}/reactivate")
async def reactivate_user(id: str):
    with Storage() as s:
        desired_user: User = s.get_one(User, {'id': id})
    
        if not desired_user:
            raise HTTPException(status_code=404)

        desired_user.disabled = False
        updated = s.update(desired_user)
    return {"reactivated_users": updated}

@user_router.delete("/")
async def deactivate_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        current_user.disabled = True
        updated = s.update(current_user)

    return {'deleted_users': updated}
