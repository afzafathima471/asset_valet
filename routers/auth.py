from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from pydantic import BaseModel

router = APIRouter()

# --- Pydantic Schemas ---
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    role: str
    username: str
    employee_id: int | None = None 

# --- Login Endpoint ---
@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint jo Supabase PostgreSQL se 
    user aur uske role ko fetch karega.
    """
    
    # 1. Database se user find karo (username filter karke)
    user = db.query(models.User).filter(models.User.username == request.username).first()

    # 2. Check: Kya user database mein exist karta hai?
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="User not found in database!"
        )

    # 3. Check: Kya password match ho raha hai?
    # (Note: Agar password hashed hai toh yahan verify_password use hoga)
    if user.password != request.password:
        raise HTTPException(
            status_code=401, 
            detail="Invalid credentials. Please check your password."
        )

    # 4. Role fetch karna:
    # Kyunki models.py mein User ke paas role_id hai, hum Role table se uska naam nikalenge
    role_info = db.query(models.Role).filter(models.Role.role_id == user.role_id).first()
    role_name = role_info.role_name if role_info else "No Role Assigned"

    # 5. Final Response
    return {
        "message": "Login successful",
        "role": role_name,
        "username": user.username,
        "employee_id" : user.employee_id
    }