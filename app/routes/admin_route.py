from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import AdminSchema
from app.services.admin_services import register_admin
router=APIRouter()

@router.post("/registeradmin")
def add_admin(admin_info:AdminSchema,db:Session=Depends(get_db)):
    if not admin_info.email or not admin_info.password or not admin_info.name or not admin_info.role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fields cannot be empty.")
    return register_admin(admin_info,db)

