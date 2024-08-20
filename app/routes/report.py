import uuid, os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from data.datastore import Storage
from data.models import Report

from settings import RESULTS_PATH

report_router = APIRouter(prefix='/reports',
                          tags=['reports'])

@report_router.get("/user/{user_id}")
def read_reports(user_id: str):
    with Storage() as s:
        relevant_reports = s.get_where(Report, {'user_id': user_id})
    return [r.dict() for r in relevant_reports]

@report_router.get('/report/{report_id}')
def report_content(report_id: str):
    with Storage() as s:
        report = s.get_one(Report, {'id': report_id})
        if not report:
            return HTMLResponse(None, status_code=404)
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

@report_router.get("/{report_id}")
def get_report(report_id: str):
    with Storage() as s:
        report = s.get_one(Report, {'id': report_id})
    return report.dict()


# GET /api/reports - List reports for the authenticated user
# GET /api/reports/{id} - Get details of a specific report
# PUT /api/reports/{id} - Update a report (e.g., to change its state)
# DELETE /api/reports/{id} - Delete a report