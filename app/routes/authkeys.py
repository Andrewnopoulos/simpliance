import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from data.datastore import Storage
from data.models import AuthKeys, User

from pydantic import BaseModel

from .auth import get_current_active_user

authkeys_router = APIRouter(prefix='/auth-keys',
                            tags=['auth-keys'])

# @authkeys_router.get("/{auth_id}")
# def read_authkeys(auth_id: str):
#     with Storage() as s:
#         authkeys = s.get_one(AuthKeys, {'id': auth_id})
#     return authkeys.dict()

# @authkeys_router.get("/user/{user_id}")
# def read_user_authkeys(user_id: str):
#     with Storage() as s:
#         user_keys = s.get_where(AuthKeys, {'user_id': user_id})
#     return [k.dict() for k in user_keys]

# @authkeys_router.post("/")
# def create_authkeys(keys: AuthKeys):
#     # TODO - generate a uid here lmao
#     with Storage() as s:
#         s.insert(keys)
#     return keys.dict()

# @authkeys_router.delete("/{auth_id}")
# def delete_authkeys(auth_id: str):
#     with Storage() as s:
#         authkeys = s.get_one(AuthKeys, {'id': auth_id})
#         if not authkeys:
#             return {"error": "authkeys not found"}
#         success = s.delete(authkeys) == 1
#         return {"retval": "success" if success else "failed"}
    
# POST /api/auth-keys - Create a new auth key
# GET /api/auth-keys - List auth keys for the authenticated user
# GET /api/auth-keys/{id} - Get details of a specific auth key
# PUT /api/auth-keys/{id} - Update an auth key
# DELETE /api/auth-keys/{id} - Delete an auth key

class NewAuthKeys(BaseModel):
    role_id: str
    external_id: str

@authkeys_router.post('/')
async def create_auth_key(new_key_data: NewAuthKeys, current_user: Annotated[User, Depends(get_current_active_user)]):
    new_authkeys = AuthKeys(
        str(uuid.uuid4()),
        new_key_data.role_id,
        new_key_data.external_id,
        current_user.id
    )
    with Storage() as s:
        s.insert(new_authkeys)
    
    return new_authkeys

@authkeys_router.get('/')
async def get_user_auth_keys(current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        user_keys = s.get_where(AuthKeys, {'user_id': current_user.id})

        return user_keys
    
@authkeys_router.get('/{id}')
async def get_auth_key(id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        user_keys = s.get_where(AuthKeys, {'user_id': current_user.id, 'id': id})

        if len(user_keys) == 1:
            return user_keys[0]
        else:
            raise HTTPException(status_code=404)


@authkeys_router.put('/{id}')
async def update_auth_key(id: str, key_data: NewAuthKeys, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        existing_key: AuthKeys = s.get_one(AuthKeys, {'user_id': current_user.id, 'id': id})

        if not existing_key:
            raise HTTPException(status_code=404)
        
        existing_key.role_id = key_data.role_id
        existing_key.external_id = key_data.external_id

        updated_keys = s.update(existing_key)

    return {"updated": updated_keys}

@authkeys_router.delete('/{id}')
async def delete_auth_key(id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        existing_key: AuthKeys = s.get_one(AuthKeys, {'user_id': current_user.id, 'id': id})

        if not existing_key:
            raise HTTPException(status_code=404)
        
        deleted_keys = s.delete(existing_key)

    return {"deleted": deleted_keys}