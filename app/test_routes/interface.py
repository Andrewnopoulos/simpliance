from fastapi import APIRouter

from data.datastore import Storage
from worker import Worker2
from data.models import AuthKeys, Report, User

interface_router = APIRouter(prefix='/run',
                             tags=['run'])

# @interface_router.post("/{auth_id}")
# def run_job(auth_id: str, benchmark_name: str):
#     with Storage() as s:
#         authkeys = s.get_one(AuthKeys, {'id': auth_id})
#         if not authkeys:
#             return {"error": f"Authkey {auth_id} not found"}
#         user = s.get_one(User, {'id': authkeys.user_id})
#         if not user:
#             return {"error": f"User {authkeys.user_id} not found"}
    
#     return Worker2().put(user, authkeys, benchmark_name)

# @interface_router.get("/list")
# def get_jobs():
#     with Storage() as s:
#         pending = s.get_where(Report, {"process_state": "pending"})
#         progress = s.get_where(Report, {"process_state": "progress"})
#         return pending + progress