from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRegister, UserLogin, UserResponse
from app.services.user_services import (
    register_user,
    login_user,
    refresh_access_token,
    delete_user_account,
)
from app.crud.users import update_users
from app.core.database import get_db
from app.core.security import is_logged_in, get_current_user
from app.models.users import UserModel

router = APIRouter()


def check_user(role: str):
    """
    Checks if the user has a "user" role. If not, raises a 400 HTTPException.

    Args:
        role (str): The role of the user.

    Raises:
        HTTPException: If the role is not "user".
    """

    if role != "user":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only Users are allowed."
        )


def validate_fields(email: str, password: str):
    """
    Validate that at least one of the fields, email or password, is provided.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Raises:
        HTTPException: If both email and password are not provided, a 400 HTTPException is raised with a
                       message indicating the need to provide at least one field.
    """

    if not email and not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please Provide an email or password to update.",
        )


def authorize_user(data_id: int, user_id: int):
    """
    Checks if the user is authorized to perform an action on the given data.

    If the user's ID does not match the data's ID, a 403 HTTPException is raised.

    Args:
        data_id (int): The ID of the data.
        user_id (int): The ID of the user.

    Raises:
        HTTPException: If the user is not authorized, a 403 HTTPException is raised with a message indicating the lack of authorization.
    """
    if data_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized."
        )


@router.get("/user", response_model=UserResponse)
def User(user: UserModel = Depends(get_current_user)):
    """
    Retrieve the current user's details.

    Args:
        user (UserModel): The current user retrieved from the access token.

    Returns:
        UserResponse: An object containing the name and email of the current user.
    """
    return UserResponse(name=user.name, email=user.email)


@router.post("/register", summary="Create a new account/Register a new user.")
def register(
    user: UserRegister, _: None = Depends(is_logged_in), db: Session = Depends(get_db)
):
    """
    Registers a new user into the database.

    Args:
        user (UserRegister): The user registration data containing name, email, password, and role.
        _ (None): A dependency check to ensure the user is not logged in.
        db (Session): The database session to use for the operation.

    Returns:
        dict: A dictionary containing a success message and the created user's details.

    Raises:
        HTTPException: If the fields are empty, a 400 status code is raised with a detail message.
    """
    return register_user(user, db)


@router.post("/login", summary="Login user")
def login(
    user: UserLogin,
    response: Response,
    _: None = Depends(is_logged_in),
    db: Session = Depends(get_db),
):
    """
    Logs in an existing user with the provided credentials.

    Args:
        user (UserLogin): The user's login credentials containing email and password.
        response (Response): The response object to set the access token.
        _ (None): A dependency check to ensure the user is not logged in.
        db (Session): The database session to use for the operation.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the user doesn't exist, a 404 status code is raised with a detail message.
                       If the password is incorrect, a 400 status code is raised with a detail message.
                       If there is an operational error during the database transaction,
                       a 500 Internal Server Error is raised indicating a database connection issue.
    """
    validate_fields(user.email, user.password)
    return login_user(user, response, db)


@router.put("/update/{user_id}", summary="Update user's info")
def update_user_info(
    user_id: int,
    user: UserLogin,
    data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates the details of an existing user in the database.

    This endpoint allows a user to update their own account information,
    such as email and password. It checks that the user has the appropriate
    "user" role, validates the provided fields, and ensures that the user
    is authorized to update the specified account.

    Args:
        user_id (int): The ID of the user to be updated.
        user (UserLogin): The new login credentials for the user.
        data (UserModel): The current user retrieved from the access token.
        db (Session): The database session to use for the operation.

    Returns:
        UserResponse: An object containing the name and email of the updated user.

    Raises:
        HTTPException: If the user role is not "user", if both email and password
                       are not provided, or if the user is not authorized to
                       update the specified account.
    """

    check_user(data.role)
    validate_fields(user.email, user.password)
    authorize_user(data.id, user_id)
    return update_users(user, data, db)


@router.delete("/delete/{user_id}", summary="Delete user's account.")
def delete_user(
    user_id: int,
    user: UserLogin,
    response: Response,
    data: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Deletes a user's account from the database.

    This endpoint allows a user to delete their own account, given the correct
    login credentials. It checks that the user has the appropriate "user" role,
    validates the provided fields, and ensures that the user is authorized to
    delete the specified account.

    Args:
        user_id (int): The ID of the user to be deleted.
        user (UserLogin): The login credentials for the user.
        response (Response): The response object to delete the access token cookie.
        data (UserModel): The current user retrieved from the access token.
        db (Session): The database session to use for the operation.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the user role is not "user", if both email and password
                       are not provided, or if the user is not authorized to
                       delete the specified account.
    """

    check_user(data.role)
    validate_fields(user.email, user.password)
    authorize_user(data.id, user_id)
    return delete_user_account(user, response, db)


@router.post("/refresh-token")
def refresh_token(request: Request, response: Response) -> dict[str, str]:
    """
    Refreshes the access token with a new one by providing a valid refresh token.

    This endpoint takes a valid refresh token from the request cookies and returns
    a new access token with a refreshed expiration time. It raises a 403 status code
    if the refresh token is not provided.

    Args:
        request (Request): The HTTP request containing the cookies.
        response (Response): The response object to set the new access token cookie.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the refresh token is not provided.
    """
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Missing refresh token."
        )
    return refresh_access_token(token, response)


@router.post("/logout")
def logout_user(response: Response, data: UserModel = Depends(get_current_user)):
    """
    Logs out the current user by deleting the access token cookie.

    This endpoint logs out the current user by deleting the access token cookie set
    in the user's browser. It retrieves the current user from the access token and
    checks that the user has the appropriate "user" role.

    Args:
        response (Response): The response object to delete the access token cookie.
        data (UserModel): The current user retrieved from the access token.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the user role is not "user".
    """
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logout Successfully."}
