from app.models.users import UserModel
from app.core.security import hash_pwd
from fastapi import HTTPException, status, Response

# from fastapi.responses import JSONResponse
from app.schemas.user_schema import UserResponse, UserRegister
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


def add_user(user: UserRegister, db: Session) -> UserResponse:
    """
    Add a new user to the database.

    Args:
        user (UserRegister): The user registration data containing name, email, password, and role.
        db (Session): The database session to use for the operation.

    Returns:
        UserResponse: An object containing the name and email of the newly added user.

    Raises:
        HTTPException: If there is an operational error during the database transaction,
                       a 500 Internal Server Error is raised indicating a database connection issue.
    """

    try:
        hashed_pwd = hash_pwd(user.password)
        data = UserModel(name=user.name, email=user.email, password=hashed_pwd)
        if user.role:
            data.role = user.role
        db.add(data)
        db.commit()
        db.refresh(data)
        return UserResponse(name=data.name, email=data.email)
    except OperationalError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database Connection Error.",
        )


def update_users(user, data, db):
    """
    Update an existing user in the database.

    Args:
        user (UserLogin): The user update data containing email and password.
        data (UserModel): The user model instance to update.
        db (Session): The database session to use for the operation.

    Returns:
        UserResponse: An object containing the name and email of the updated user.

    Raises:
        HTTPException: If there is an internal server error during the database transaction,
                       a 500 Internal Server Error is raised indicating a server error.
    """
    try:
        if user.email:
            data.email = user.email
        if user.password:
            data.password = hash_pwd(user.password)
        db.commit()
        db.refresh(data)
        return UserResponse(name=data.name, email=data.email)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error.",
        )


def delete_users(
    user_data: UserModel, response: Response, db: Session
) -> dict[str, str]:
    """
    Delete a user from the database.

    Args:
        user_data (UserModel): The user model instance to delete.
        response (Response): The response object to delete the access token cookie.
        db (Session): The database session to use for the operation.

    Returns:
        dict[str, str]: A dictionary containing a success message.

    Raises:
        HTTPException: If there is an operational error during the database transaction,
                       a 500 Internal Server Error is raised indicating a server error.
    """

    try:
        db.delete(user_data)
        db.commit()
        response.delete_cookie("access_token")
        return {"message": "User Deleted Successfully."}
    except OperationalError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection issue.",
        )
