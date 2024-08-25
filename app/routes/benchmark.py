import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from data.datastore import Storage
from data.models import AuthKeys, User
from worker import Worker2

from pydantic import BaseModel

from .auth import get_current_active_user

from client import VALID_BENCHMARKS

benchmark_router = APIRouter(prefix='/benchmark',
                            tags=['benchmark'])

@benchmark_router.get("/")
def get_benchmark_list():
    return VALID_BENCHMARKS

class newBenchmarkReport(BaseModel):
    auth_key_id: str
    type: str

@benchmark_router.post("/")
def start_benchmarking(benchmark_details: newBenchmarkReport, current_user: Annotated[User, Depends(get_current_active_user)]):
    
    if benchmark_details.type not in VALID_BENCHMARKS:
        raise HTTPException(status_code=404, detail="Benchmark does not exist")
    
    with Storage() as s:
        auth_key = s.get_one(AuthKeys, {'id': benchmark_details.auth_key_id})

    if not auth_key:
        raise HTTPException(status_code=404, detail=f"Auth key with id {benchmark_details.auth_key_id} not found")
    
    if auth_key.user_id != current_user.id:
        raise HTTPException(status_code=404, detail=f"Auth key with id {benchmark_details.auth_key_id} not found")
    
    return Worker2().put(current_user, auth_key, benchmark_details.type)
