import uuid

from fastapi import APIRouter

from data.datastore import Storage
from data.models import Report

report_router = APIRouter(prefix='/reports',
                          tags=['reports'])

@report_router.get("/{user_id}")
def read_reports(user_id: str):
    with Storage() as s:
        relevant_reports = s.get_where(Report, {'user_id': user_id})
    return [r.dict() for r in relevant_reports]

@report_router.get("/report/{report_id}")
def get_report(report_id: str):
    with Storage() as s:
        report = s.get_one(Report, {'id': report_id})
    return report.dict()

@report_router.post("/{user_id}")
def create_report(user_id: str):
    with Storage() as s:
        new_report = Report(str(uuid.uuid4()), "pending", "now", "", user_id)
        s.insert(new_report)
    return new_report.dict()