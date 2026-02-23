from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String)
    designation = Column(String)
    joining_date = Column(Date)

from sqlalchemy import Column, Integer, String, Date

class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    asset_type = Column(String)
    purchase_date = Column(Date)
    status = Column(String, default="Available")