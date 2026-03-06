from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models


# Temporary user simulation (later JWT token will replace this)
def get_current_user(db: Session = Depends(get_db)):
    user = db.query(models.User).first()
    return user


def RequirePrivilege(required_permission: str):

    def privilege_checker(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        role = db.query(models.Role).filter(
            models.Role.role_id == current_user.role_id
        ).first()

        role_permissions = db.query(models.RolePermission).filter(
            models.RolePermission.role_id == role.role_id
        ).all()

        permission_ids = [rp.permission_id for rp in role_permissions]

        permissions = db.query(models.Permission).filter(
            models.Permission.permission_id.in_(permission_ids)
        ).all()

        permission_names = [p.permission_name for p in permissions]

        if required_permission not in permission_names:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action"
            )

        return True

    return privilege_checker