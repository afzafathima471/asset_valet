from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from pydantic import BaseModel
from datetime import date
from typing import Optional

router = APIRouter()

class ConditionReportCreate(BaseModel):
    asset_id: int
    report_date: date
    condition_status: str
    description: str
    action_taken: Optional[str] = None
    reported_by: Optional[str] = None
    image: Optional[str] = None

class ConditionReportResponse(ConditionReportCreate):
    id: int

    class Config:
        from_attributes = True

@router.post("/condition-reports", response_model=ConditionReportResponse)
def create_report(report: ConditionReportCreate, db: Session = Depends(get_db)):
    """Submit asset condition report"""
    asset = db.query(models.Asset).filter(models.Asset.asset_id == report.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db_report = models.ConditionReport(
        asset_id=report.asset_id,
        report_date=report.report_date,
        condition_status=report.condition_status,
        description=report.description,
        action_taken=report.action_taken,
        reported_by=report.reported_by,
        image=report.image,
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/condition-reports")
def get_all_reports(db: Session = Depends(get_db)):
    """Get all condition reports"""
    return db.query(models.ConditionReport).all()