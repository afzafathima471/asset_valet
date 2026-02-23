from fastapi import FastAPI
from app import models
from app.database import engine
from routers import employees, assets  
# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Asset Management API")

# Include Routers with optional prefix and tags
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(assets.router, prefix="/api/assets", tags=["Assets"])