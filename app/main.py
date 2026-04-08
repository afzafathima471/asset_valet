from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from routers import employees, assets, assignments, auth, condition_reports

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Asset Valet API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000" , "https://frontend-eight-rho-68.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(auth.router)
app.include_router(condition_reports.router)