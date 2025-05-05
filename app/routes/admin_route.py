from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import AdminSchema, UserLogin
from app.services.admin_services import register_admin, login_admin
from app.core.security import is_logged_in

router = APIRouter()


@router.post("/admin/register")
def add_admin(
    admin_info: AdminSchema,
    _: None = Depends(is_logged_in),
    db: Session = Depends(get_db),
):
    
    if (
        not admin_info.email
        or not admin_info.password
        or not admin_info.name
        or not admin_info.role
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Fields cannot be empty."
        )
    return register_admin(admin_info, db)


@router.post("/admin/login")
def login_admin_account(
    admin_info: UserLogin,
    response: Response,
    _: None = Depends(is_logged_in),
    db: Session = Depends(get_db),
):
    if not admin_info.email or not admin_info.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields should not be empty.",
        )
    return login_admin(admin_info, response, db)
