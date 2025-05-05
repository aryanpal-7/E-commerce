from fastapi import status, HTTPException
from app.models.users import UserModel
from app.crud.users import add_user
from app.core.security import create_access_token, set_access_token


def register_admin(admin_data, db):
    data = (
        db.query(UserModel)
        .filter(UserModel.email == admin_data.email, UserModel.role == "admin")
        .first()
    )
    if data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Admin Already Exists."
        )
    return add_user(admin_data, db)


def login_admin(admin_data, response, db):
    data = (
        db.query(UserModel)
        .filter(UserModel.email == admin_data.email, UserModel.role == "admin")
        .first()
    )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin doesn't Exists."
        )
    token = create_access_token(dict({"sub": str(data.id)}))
    set_access_token(response, token)
    return {"message": "Admin Logged in Successfully."}
