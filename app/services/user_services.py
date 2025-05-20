# Register, login, Update info, Delete User
from fastapi import HTTPException, status, Response
from app.models.users import UserModel
from app.crud.users import add_user
from app.core.security import (
    verify_pwd,
    create_access_token,
    create_refresh_token,
    set_access_token,
    set_refresh_token,
)
from sqlalchemy.exc import OperationalError
from app.crud.users import delete_users
from app.schemas.user_schema import UserRegister, UserLogin
from sqlalchemy.orm import Session
from jose import JWTError, jwt


REFRESH_TOKEN_SECRET = "secretrefresh"
ALGORITHM = "HS256"


def raise_http(status_code: int, detail: str):
    """
    Raises an HTTPException with the given status code and detail message.
    Intended to be used to raise an exception when something goes wrong
    in the business logic of the API, as opposed to a low-level error
    that can be caught and handled by the framework.
    """

    raise HTTPException(status_code=status_code, detail=detail)


def register_user(user: UserRegister, db: Session):
    """
    Registers a new user into the database.

    Args:
        user (UserRegister): The user registration data containing name, email, password, and role.
        db (Session): The database session to use for the operation.

    Returns:
        dict: A dictionary containing a success message and the created user's details.

    Raises:
        HTTPException: If the user already exists, a 409 status code is raised with a detail message.
    """

    data = db.query(UserModel).filter(UserModel.email == user.email).first()
    if data:
        raise_http(status.HTTP_409_CONFLICT, "User already exist!")
    return add_user(user, db)


def login_user(user: UserLogin, response: Response, db: Session) -> dict[str, str]:
    """
    Logs in an existing user with the provided credentials.

    Args:
        user (UserLogin): The user's login credentials.
        response (Response): The response object to set the access token.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the user doesn't exist, a 404 status code is raised with a detail message.
                      If the password is incorrect, a 400 status code is raised with a detail message.
                      If there is an operational error during the database transaction,
                      a 500 Internal Server Error is raised indicating a database connection issue.
    """
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
            raise_http(status.HTTP_401_UNAUTHORIZED, "Password incorrect.")
        token = create_access_token(data=({"sub": str(data.id)}))
        refresh_token = create_refresh_token(data=({"sub": str(data.id)}))
        set_access_token(response, token)
        set_refresh_token(response, refresh_token)

        return {"message": "Login Successful"}
    except OperationalError:
        db.rollback()
        raise_http(status.HTTP_500_INTERNAL_SERVER_ERROR, "Database error.")


def refresh_access_token(token: str, response: Response) -> dict[str, str]:
    """
    Refreshes the access token using a valid refresh token.

    This function decodes the provided refresh token to extract the user ID,
    and generates a new access token with refreshed expiration time. The new
    access token is then set in the response cookies.

    Args:
        token (str): The refresh token to be decoded.
        response (Response): The response object to set the new access token cookie.

    Returns:
        dict: A dictionary containing a success message indicating the access token has been refreshed.

    Raises:
        HTTPException: If the token payload is invalid or the refresh token is invalid,
                       a 403 status code is raised with a detail message.
    """

    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise_http(status.HTTP_403_FORBIDDEN, "Invalid token payload.")

        new_access_token = create_access_token({"sub": user_id})
        set_access_token(response, new_access_token)

        return {"message": "Access token refreshed"}
    except JWTError:
        raise_http(status.HTTP_403_FORBIDDEN, "Invalid refresh token.")


def delete_user_account(
    user: UserLogin, response: Response, db: Session
) -> dict[str, str]:
    """
    Deletes a user's account from the database.

    Args:
        user (UserLogin): The user's login credentials containing email and password.
        response (Response): The response object to delete the access token cookie.
        db (Session): The database session to use for the operation.

    Returns:
        dict[str, str]: A dictionary containing a success message.

    Raises:
        HTTPException: If the user is not found, a 404 status code is raised.
                       If the password is incorrect, a 400 status code is raised.
    """

    user_data = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not user_data:
        raise_http(status.HTTP_404_NOT_FOUND, "User not found")
    check_pwd = verify_pwd(user.password, user_data.password)
    if not check_pwd:
        raise_http(status.HTTP_400_BAD_REQUEST, "Password Incorrect.")
    return delete_users(user_data, response, db)
