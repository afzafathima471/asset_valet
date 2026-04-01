from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from pydantic import BaseModel
from datetime import date
from typing import Optional

router = APIRouter()

class AssignmentCreate(BaseModel):
    asset_id: int
    employee_id: int
    assignment_date: date
    expected_return_date: Optional[date] = None
    initial_condition: Optional[str] = None
    notes: Optional[str] = None

class AssignmentResponse(AssignmentCreate):
    id: int
    actual_return_date: Optional[date] = None
    return_condition: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/assignments", response_model=AssignmentResponse)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """Assign an asset to an employee."""
    # Check asset exists
    asset = db.query(models.Asset).filter(models.Asset.asset_id == assignment.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Check employee exists
    employee = db.query(models.Employee).filter(models.Employee.employee_id == assignment.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Create assignment
    db_assignment = models.AssetAssignment(
        asset_id=assignment.asset_id,
        employee_id=assignment.employee_id,
        assignment_date=assignment.assignment_date,
        expected_return_date=assignment.expected_return_date,
        initial_condition=assignment.initial_condition,
        notes=assignment.notes
    )
    db.add(db_assignment)
    
    # Update asset status to Assigned
    asset.status = "Assigned"
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/assignments")
def get_all_assignments(db: Session = Depends(get_db)):
    """Get all assignments."""
    return db.query(models.AssetAssignment).all()

@router.get("/assignments/{assignment_id}")
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Get assignment by ID."""
    assignment = db.query(models.AssetAssignment).filter(
        models.AssetAssignment.id == assignment_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment