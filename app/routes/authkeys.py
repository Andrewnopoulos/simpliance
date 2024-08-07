from fastapi import APIRouter

from data.datastore import Storage
from data.models import AuthKeys

authkeys_router = APIRouter(prefix='/authkeys',
                            tags=['authkeys'])

@authkeys_router.get("/{auth_id}")
def read_authkeys(auth_id: str):
    with Storage() as s:
        authkeys = s.get_one(AuthKeys, {'id': auth_id})
    return authkeys.dict()

@authkeys_router.get("/user/{user_id}")
def read_user_authkeys(user_id: str):
    with Storage() as s:
        user_keys = s.get_where(AuthKeys, {'user_id': user_id})
    return [k.dict() for k in user_keys]

@authkeys_router.post("/")
def create_authkeys(keys: AuthKeys):
    with Storage() as s:
        s.insert(keys)
    return keys.dict()

@authkeys_router.delete("/{auth_id}")
def delete_authkeys(auth_id: str):
    with Storage() as s:
        authkeys = s.get_one(AuthKeys, {'id': auth_id})
        if not authkeys:
            return {"error": "authkeys not found"}
        success = s.delete(authkeys) == 1
        return {"retval": "success" if success else "failed"}