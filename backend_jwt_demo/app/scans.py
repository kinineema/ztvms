from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from time import sleep
from typing import List, Literal, Optional
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, get_db
from .deps import get_current_user

router = APIRouter(prefix="/scans", tags=["scans"])

class StartScanIn(BaseModel):
    target_url: HttpUrl

class FindingOut(BaseModel):
    id: int
    tool: str
    name: str
    risk: str
    url: str
    param: Optional[str] = None
    evidence: str

    model_config = ConfigDict(from_attributes=True)

class StartScanOut(BaseModel):
    scan_id: int = Field(..., alias='id')
    target_url: str
    status: Literal["queued", "running", "done", "failed"] = "queued"
    user_id: int
    findings: List[FindingOut] = []

    model_config = ConfigDict(from_attributes=True)

def _run_scan(scan_id: int, target_url: str):
    db = SessionLocal()
    try:
        scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
        if not scan:
            return

        # Update status to running
        scan.status = "running"
        db.commit()

        sleep(4)  # simulate scan time
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
        for finding in findings:
            db_finding = models.Finding(**finding, scan_id=scan.id)
            db.add(db_finding)
        scan.status = "done"
        db.commit()
    finally:
        db.close()

@router.post("", response_model=StartScanOut)
def start_scan(body: StartScanIn, bg: BackgroundTasks, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role == "viewer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to start scans")

    new_scan = models.Scan(
        target_url=str(body.target_url),
        status="queued",
        user_id=user.id
    )
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    bg.add_task(_run_scan, new_scan.id, str(body.target_url))

    return new_scan

@router.get("/{scan_id}/status")
def scan_status(scan_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Not found")
    return {"scan_id": scan_id, "status": scan.status}

@router.get("/{scan_id}/report", response_model=StartScanOut)
def scan_report(scan_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != user.id and user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to view this report")
    return scan