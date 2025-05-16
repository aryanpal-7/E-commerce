from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import AdminSchema, UserLogin
from app.services.admin_services import register_admin, login_admin
from app.core.security import is_logged_in

router = APIRouter()


@router.post("/register")
def add_admin(
    admin_info: AdminSchema,
    _: None = Depends(is_logged_in),
    db: Session = Depends(get_db),
):
    """
    Registers a new admin user into the database.

    Args:
        admin_info (AdminSchema): The admin's details to be registered.
        _ (None): A dependency check to ensure the user is not logged in.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message and the created admin's details.

    Raises:
        HTTPException: If the fields are empty, a 400 status code is raised with a detail message.
    """

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


@router.post("/login")
def login_admin_account(
    admin_info: UserLogin,
    response: Response,
    _: None = Depends(is_logged_in),
    db: Session = Depends(get_db),
):
    """
    Logs in an admin user with the provided credentials.

    Args:
        admin_info (UserLogin): The admin's login credentials.
        response (Response): The response object to set the access token.
        _ (None): A dependency check to ensure the user is not logged in.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message and the access token.

    Raises:
        HTTPException: If the fields are empty, a 400 status code is raised with a detail message.
    """
    if not admin_info.email or not admin_info.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields should not be empty.",
        )
    return login_admin(admin_info, response, db)
