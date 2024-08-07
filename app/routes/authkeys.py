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
