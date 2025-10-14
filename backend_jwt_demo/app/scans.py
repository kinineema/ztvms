# app/scans.py
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from uuid import uuid4
from time import sleep
from typing import Literal, Dict
from .deps import get_current_user

router = APIRouter(prefix="/scans", tags=["scans"])

# in-memory storage (demo)
SCANS: Dict[str, Dict] = {}  # scan_id -> {status, target, findings}

class StartScanIn(BaseModel):
    target_url: HttpUrl

class StartScanOut(BaseModel):
    scan_id: str
    status: Literal["queued", "running", "done", "failed"] = "queued"

def _run_scan(scan_id: str, target_url: str):
    # simulate work
    SCANS[scan_id]["status"] = "running"
    sleep(4)  # pretend scan time
    # demo findings
    findings = [
        {
            "tool": "zap",
            "name": "X-Content-Type-Options Header Missing",
            "risk": "Low",
            "url": str(target_url),
            "param": None,
            "evidence": "Header not set",
        },
        {
            "tool": "zap",
            "name": "Cookie Without Secure Flag",
            "risk": "Medium",
            "url": f"{target_url.rstrip('/')}/login",
            "param": "sessionid",
            "evidence": "Set-Cookie: sessionid=...; HttpOnly",
        },
    ]
    SCANS[scan_id]["findings"] = findings
    SCANS[scan_id]["status"] = "done"

@router.post("", response_model=StartScanOut)
def start_scan(body: StartScanIn, bg: BackgroundTasks, user=Depends(get_current_user)):
    # RBAC: viewers cannot start scans
    if user["role"] == "viewer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to start scans")
    scan_id = str(uuid4())
    SCANS[scan_id] = {"status": "queued", "target": str(body.target_url), "findings": []}
    bg.add_task(_run_scan, scan_id, str(body.target_url))
    return {"scan_id": scan_id, "status": "queued"}

@router.get("/{scan_id}/status")
def scan_status(scan_id: str, user=Depends(get_current_user)):
    rec = SCANS.get(scan_id)
    if not rec: raise HTTPException(status_code=404, detail="Not found")
    return {"scan_id": scan_id, "status": rec["status"]}

@router.get("/{scan_id}/report")
def scan_report(scan_id: str, user=Depends(get_current_user)):
    rec = SCANS.get(scan_id)
    if not rec: raise HTTPException(status_code=404, detail="Not found")
    if rec["status"] != "done":
        raise HTTPException(status_code=409, detail="Report not ready")
    return {"scan_id": scan_id, "target": rec["target"], "findings": rec["findings"]}
