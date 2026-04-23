from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres.dskuuydnlsfuzouppyom:shdje23$%^&df@aws-1-ap-south-1.pooler.supabase.com:5432/postgres")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()