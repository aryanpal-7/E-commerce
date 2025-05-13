from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRegister, UserLogin, UserResponse
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
    if role != "user":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only Users are allowed."
        )


def validate_fields(email: str, password: str):
    if not email and not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please Provide an email or password to update.",
        )


def authorize_user(data_id, user_id):
    if data_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized."
        )


@router.get("/user", response_model=UserResponse)
def User(user: UserModel = Depends(get_current_user)):

    return UserResponse(name=user.name, email=user.email)


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
    validate_fields(user.email, user.password)
    return login_user(user, response, db)


@router.put("/user/{user_id}", summary="Update user's info")
def update_user_info(
    user_id: int,
    user: UserLogin,
    data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_user(data.role)
    validate_fields(user.email, user.password)
    authorize_user(data.id, user_id)
    return update_users(user, data, db)


@router.delete("/user/{user_id}", summary="Delete user's account.")
def delete_user(
    user_id: int,
    user: UserLogin,
    response: Response,
    data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_user(data.role)
    validate_fields(user.email, user.password)
    authorize_user(data.id, user_id)
    return delete_user_account(user, response, db)


@router.post("/logout")
def logout_user(response: Response, data: UserModel = Depends(get_current_user)):

    response.delete_cookie("access_token")
    return {"message": "Logout Successfully."}
