# Register, login, Update info, Delete User
from fastapi import HTTPException, status
from app.models.users import UserModel
from app.crud.users import add_user
from app.core.security import verify_pwd, create_access_token, set_access_token
from sqlalchemy.exc import OperationalError
from app.crud.users import delete_users


def raise_http(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)


def register_user(user, db):
    data = db.query(UserModel).filter(UserModel.email == user.email).first()
    if data:
        raise_http(status.HTTP_409_CONFLICT, "User already exist!")
    return add_user(user, db)


def login_user(user, response, db):
    try:
        data = (
            db.query(UserModel)
            .filter(UserModel.email == user.email, UserModel.role == "user")
            .first()
        )
        if not data:
            raise_http(status.HTTP_404_NOT_FOUND, "User doesn't exists.")
        check_pwd = verify_pwd(user.password, data.password)
        if not check_pwd:
            raise_http(status.HTTP_400_BAD_REQUEST, "Password incorrect.")
        token = create_access_token(data=({"sub": str(data.id)}))
        set_access_token(response, token)
        return {"message": "Login Successful"}
    except OperationalError:
        db.rollback()
        raise_http(status.HTTP_500_INTERNAL_SERVER_ERROR, "Database error.")


def delete_user_account(user, db):
    user_data = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not user_data:
        raise_http(status.HTTP_404_NOT_FOUND, "User not found")
    check_pwd = verify_pwd(user.password, user_data.password)
    if not check_pwd:
        raise_http(status.HTTP_400_BAD_REQUEST, "Password Incorrect.")
    return delete_users(user_data, db)
