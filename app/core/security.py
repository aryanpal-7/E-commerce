# JWT generation, hash and verify password, current user logic
from fastapi import Request, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.models.users import UserModel
from app.core.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE = 30
SECRET_KEY = "secret"
ALGORITHM = "HS256"


def hash_pwd(password: str) -> str:
    """Hash the given password with a secure hash algorithm.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_pwd(password: str, hashed_pwd: str) -> bool:
    """Verify that the given password matches the hashed password.

    Args:
        password (str): The password to verify.
        hashed_pwd (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(password, hashed_pwd)


def create_access_token(data: dict) -> str:
    """Generate a JWT token for the given data.

    Args:
        data (dict): The data to encode in the JWT token.

    Returns:
        str: The JWT token.
    """

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def set_access_token(response: Response, token: str):
    """Set the given JWT token as an HTTPOnly cookie in the response.

    Args:
        response (Response): The response to set the cookie in.
        token (str): The JWT token to set as the cookie value.
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800,
    )


def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserModel:
    """Retrieve the current user based on the access token in the request cookies.

    Args:
        request (Request): The HTTP request containing the cookies.
        db (Session): The database session dependency.

    Returns:
        UserModel: The user model instance corresponding to the token's subject.

    Raises:
        HTTPException: If the access token is missing, expired, invalid, or if the user is not found.
    """

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please Login Before continuing.",
        )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=ALGORITHM, options={"verify_signature": True}
        )
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token missing or expired.",
            )
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token expired. Login again.",
            )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
    data = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found."
        )
    return data


def is_logged_in(request: Request) -> dict[str, str] | None:
    """Check if a user is already logged in.

    Args:
        request (Request): The HTTP request containing the cookies.

    Returns:
        dict[str, str] | None: The error message if the user is already logged in or None if the user is not logged in.
    """
    token = request.cookies.get("access_token")

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Session already Logged in.",
                )
        except JWTError as e:
            return {"message": f"some error occured: {e}"}
