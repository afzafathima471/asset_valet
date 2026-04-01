from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    role: str
    name: str

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint"""
    # Hardcoded users for demo
    users = {
        "admin": {"password": "admin123", "role": "admin", "name": "Afza (Admin)"},
        "employee": {"password": "emp123", "role": "employee", "name": "Rahul Sharma"},
    }
    
    user = users.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {
        "message": "Login successful",
        "role": user["role"],
        "name": user["name"]
    }