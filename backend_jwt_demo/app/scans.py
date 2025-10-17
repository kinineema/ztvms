# app/scans.py
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
from uuid import uuid4
from typing import Literal, Dict, Optional, Any
from .deps import get_current_user
from .zap_service import run_zap_scan  # real ZAP integration

router = APIRouter(prefix="/scans", tags=["scans"])

# in-memory storage (demo):
# scan_id -> {status, target, findings, error?}
SCANS: Dict[str, Dict[str, Any]] = {}

# ---------- Schemas ----------

class StartScanIn(BaseModel):
    # accept either key from the frontend
    target_url: Optional[str] = None
    target: Optional[str] = None

class StartScanOut(BaseModel):
    scan_id: str
    status: Literal["queued", "running", "done", "failed"] = "queued"

# ---------- Worker ----------

def _run_scan(scan_id: str, target_url: str):
    """
    Background job:
    - runs real ZAP scan (bounded/time-limited in zap_service.py)
    - stores normalized findings
    - marks final status done/failed
    """
    try:
        SCANS[scan_id]["status"] = "running"

        alerts = run_zap_scan(target_url)

        findings = [
            {
                "tool": "ZAP",
                "name": a.get("alert"),
                "risk": a.get("risk"),
                "url": a.get("url"),
                "param": a.get("param"),
                "evidence": a.get("evidence"),
            }
            for a in (alerts or [])
        ]
        SCANS[scan_id]["findings"] = findings
        SCANS[scan_id]["status"] = "done"

    except Exception as e:
        SCANS[scan_id]["status"] = "failed"
        SCANS[scan_id]["error"] = str(e)

# ---------- Routes ----------

@router.post("", response_model=StartScanOut)
def start_scan(body: StartScanIn, bg: BackgroundTasks, user=Depends(get_current_user)):
    # RBAC: viewers cannot start scans
    if user["role"] == "viewer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to start scans"
        )

    # Coalesce keys from the frontend
    raw = (body.target or body.target_url or "").strip()
    if not raw:
        raise HTTPException(status_code=400, detail="Missing 'target' or 'target_url'")

    # Normalize scheme for users who type "example.com"
    if not raw.startswith(("http://", "https://")):
        raw = "http://" + raw

    scan_id = str(uuid4())
    SCANS[scan_id] = {"status": "queued", "target": raw, "findings": []}
    bg.add_task(_run_scan, scan_id, raw)
    return {"scan_id": scan_id, "status": "queued"}

@router.get("/{scan_id}/status")
def scan_status(scan_id: str, user=Depends(get_current_user)):
    rec = SCANS.get(scan_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Not found")
    resp = {"scan_id": scan_id, "status": rec["status"]}
    if rec["status"] == "failed" and "error" in rec:
        resp["error"] = rec["error"]
    return resp

@router.get("/{scan_id}/report")
def scan_report(scan_id: str, user=Depends(get_current_user)):
    rec = SCANS.get(scan_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Not found")
    if rec["status"] != "done":
        raise HTTPException(status_code=409, detail="Report not ready")
    return {"scan_id": scan_id, "target": rec["target"], "findings": rec["findings"]}
