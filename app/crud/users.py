from app.models.users import UserModel
from app.core.security import hash_pwd
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError


def add_user(user, db):
    try:
        hashed_pwd = hash_pwd(user.password)
        data = UserModel(name=user.name, email=user.email, password=hashed_pwd)
        if user.role:
            data.role=user.role
        db.add(data)
        db.commit()
        db.refresh(data)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User Registered Successfully", "data": data.name},
        )
    except OperationalError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Connection Error.",
        )


def update_users(user, data, db):
    if user.email:
        data.email = user.email
    if user.password:
        data.password = hash_pwd(user.password)
    db.commit()
    db.refresh(data)
    return {"message": "Update data successfully", "data": data}


def delete_users(user_obj, db):
    try:
        db.delete(user_obj)
        db.commit()
        return {"message": "User Deleted Successfully."}
    except OperationalError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection issue.",
        )
