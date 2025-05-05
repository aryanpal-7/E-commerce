from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRegister, UserLogin
from app.services.auth_services import register_user, login_user, delete_user_account
from app.crud.users import update_users
from app.core.database import get_db
from app.core.security import is_logged_in, get_current_user
from app.models.users import UserModel

router = APIRouter()


"""
    1.Add Response Models 
"""

def check_user(role):
    if role!="user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Users are allowed.")

@router.get("/user")
def User(user:UserModel=Depends(get_current_user)):
    check_user(user.role)
    return {"name": user.name, "email":user.email}


@router.post("/register", summary="Create a new account/Register a new user.")
def register(
    user: UserRegister, _: None = Depends(is_logged_in), db: Session = Depends(get_db)
):
    return register_user(user, db)


@router.post("/login", summary="Login user")
def login(
    user: UserLogin,
    response: Response,
    _: None = Depends(is_logged_in),
    db: Session = Depends(get_db),
):
    if not user.email or not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields should not be empty.",
        )
    return login_user(user, response, db)


@router.put("/user/{user_id}", summary="Update user's info")
def update_user_info(
    user_id: int,
    user: UserLogin,
    data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_user(data.role)
    if not user.email and not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please Provide an email or password to update.",
        )
    if data.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized."
        )
    return update_users(user, data, db)


@router.delete("/user/{user_id}", summary="Delete user's account.")
def delete_user(
    user_id: int,
    user: UserLogin,
    data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_user(data.role)
    if not user.email or not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Fields can't be empty"
        )
    if data.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    return delete_user_account(user, db)


@router.post("/logout")
def logout_user(response: Response, data: UserModel = Depends(get_current_user)):
    check_user(data.role)
    response.delete_cookie("access_token")
    return {"message": "Logout Successfully."}
