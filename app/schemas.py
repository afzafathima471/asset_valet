from pydantic import BaseModel
from datetime import date


class EmployeeBase(BaseModel):
    name: str
    department: str
    designation: str
    joining_date: date


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    employee_id: int

    class Config:
        orm_mode = True

        
class AssetBase(BaseModel):
    name: str
    asset_type: str
    purchase_date: date
    status: str


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: str | None = None
    asset_type: str | None = None
    purchase_date: date | None = None
    status: str | None =None
    current_condition: str | None = None 
    pass


class AssetResponse(AssetBase):
    asset_id: int

    class Config:
        from_attributes = True