from fastapi import status, HTTPException, Response
from app.models.users import UserModel
from app.crud.users import add_user
from app.core.security import (
    create_access_token,
    set_access_token,
    create_refresh_token,
    set_refresh_token,
    verify_pwd,
)
from app.schemas.user_schema import AdminSchema, UserLogin, UserResponse
from sqlalchemy.orm import Session


def register_admin(admin_data: AdminSchema, db: Session) -> UserResponse:
    """
    Registers a new admin user into the database.

    Args:
        admin_data (AdminSchema): The admin's details to be registered.
        db (Session): The database session.

    Returns:
        UserResponse: An object containing the name and email of the newly added admin user.

    Raises:
        HTTPException: If the admin already exists, a 409 status code is raised with a detail message.
    """
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


def login_admin(
    admin_data: UserLogin, response: Response, db: Session
) -> dict[str, str]:
    """
    Logs in an admin user with the provided credentials.

    Args:
        admin_data (UserLogin): The admin's login credentials.
        response (Response): The response object to set the access token.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the admin doesn't exists, a 404 status code is raised with a detail message.
    """

    data = (
        db.query(UserModel)
        .filter(UserModel.email == admin_data.email, UserModel.role == "admin")
        .first()
    )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin doesn't Exists."
        )
    check_pwd = verify_pwd(admin_data.password, data.password)
    if not check_pwd:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password."
        )
    token = create_access_token(dict({"sub": str(data.id)}))
    refresh_token = create_refresh_token(dict({"sub": str(data.id)}))
    set_access_token(response, token)
    set_refresh_token(response, refresh_token)
    return {"message": "Admin Logged in Successfully."}
