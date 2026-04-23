from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
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

# ==============================
# RBAC TABLES
# ==============================

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)


class Permission(Base):
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String, unique=True, index=True)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=True)
    role = relationship("Role")

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    permission_id = Column(Integer, ForeignKey("permissions.permission_id"))

class AssetAssignment(Base):
    __tablename__ = "asset_assignments"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"))
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    assignment_date = Column(Date)
    expected_return_date = Column(Date, nullable=True)
    actual_return_date = Column(Date, nullable=True)
    initial_condition = Column(String, nullable=True)
    return_condition = Column(String, nullable=True)
    notes = Column(String, nullable=True)

class ConditionReport(Base):
    __tablename__ = "condition_reports"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"))
    report_date = Column(Date)
    condition_status = Column(String)
    description = Column(String)
    action_taken = Column(String, nullable=True)
    reported_by = Column(String, nullable=True)
    image = Column(String, nullable=True)