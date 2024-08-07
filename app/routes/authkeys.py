from fastapi import APIRouter

from data.datastore import Storage
from data.models import AuthKeys

authkeys_router = APIRouter(prefix='/authkeys',
                            tags=['authkeys'])

@authkeys_router.get("/{user_id}")
def read_authkeys(user_id: str):
    with Storage() as s:
        authkeys = s.get_where(AuthKeys, {'user_id': user_id})
    return [k.dict() for k in authkeys]

@authkeys_router.post("/{user_id}")
def create_authkeys(user_id: str, keys: AuthKeys):
    with Storage() as s:
        s.insert(keys)
    return keys.dict()

@authkeys_router.delete("/{user_id}/{role_id}")
def delete_authkeys(user_id: str, role_id: str):
    with Storage() as s:
        authkeys = s.get_one(AuthKeys, {'role_id': role_id})
        if not authkeys:
            return {"error": "authkeys not found"}
        success = s.delete(authkeys) == 1
        return {"retval": "success" if success else "failed"}