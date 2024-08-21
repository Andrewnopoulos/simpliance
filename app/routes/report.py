import uuid, os

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from data.datastore import Storage, User
from data.models import Report

from .auth import get_password_hash, get_current_active_user

from settings import RESULTS_PATH

report_router = APIRouter(prefix='/reports',
                          tags=['reports'])

# @report_router.get("/user/{user_id}")
# def read_reports(user_id: str):
#     with Storage() as s:
#         relevant_reports = s.get_where(Report, {'user_id': user_id})
#     return [r.dict() for r in relevant_reports]

# @report_router.get('/report/{report_id}')
# def report_content(report_id: str):
#     with Storage() as s:
#         report = s.get_one(Report, {'id': report_id})
#         if not report:
#             return HTMLResponse(None, status_code=404)
#         if report.process_state == "done":
#             filename = os.path.join(RESULTS_PATH, f"{report_id}.html")
#             print(f"searching for {filename}")
#             try:
#                 with open(filename, 'r') as f:
#                     html_content = f.read()
#                 return HTMLResponse(content=html_content, status_code=200)
#             except:
#                 return JSONResponse({"error": f"Failed to find {filename}"})
#         else:
#             return report

# @report_router.get("/{report_id}")
# def get_report(report_id: str):
#     with Storage() as s:
#         report = s.get_one(Report, {'id': report_id})
#     return report.dict()

# GET /api/reports - List reports for the authenticated user
# GET /api/reports/{id} - Get details of a specific report
# PUT /api/reports/{id} - Update a report (e.g., to change its state)
# DELETE /api/reports/{id} - Delete a report

@report_router.get("/")
def get_reports(current_user: Annotated[User, Depends(get_current_active_user)]) -> list[Report]:
    with Storage() as s:
        reports_for_user = s.get_where(Report, {'user_id': current_user.id})

    return reports_for_user

@report_router.get("/{report_id}")
def get_report_by_id(report_id: str, current_user: Annotated[User, Depends(get_current_active_user)]) -> Report:
    with Storage() as s:
        report_data: Report = s.get_one(Report, {'id': report_id, 'user_id': current_user.id})
    
    if not report_data:
        raise HTTPException(status_code=404)
    
    return report_data

@report_router.get("/{report_id}/content")
def get_report_content(report_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        report = s.get_one(Report, {'id': report_id, "user_id": current_user.id})
        if not report:
            return HTMLResponse(f"Could not find report with id {report_id} under user {current_user.name}", status_code=404)
        if report.process_state == "done":
            filename = os.path.join(RESULTS_PATH, f"{report_id}.html")
            print(f"searching for {filename}")
            try:
                with open(filename, 'r') as f:
                    html_content = f.read()
                return HTMLResponse(content=html_content, status_code=200)
            except:
                return JSONResponse({"error": f"Failed to find {filename}"})
        else:
            return report

@report_router.delete("/{report_id}")
def delete_report(report_id: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with Storage() as s:
        report_data: Report = s.get_one(Report, {'id': report_id, 'user_id': current_user.id})
    
        if not report_data:
            raise HTTPException(status_code=404)
        
        report_path = os.path.join(RESULTS_PATH, f"{report_data.id}.html")
        os.remove(report_path)

        deleted = s.delete(report_data)

    return {'deleted_reports': deleted}