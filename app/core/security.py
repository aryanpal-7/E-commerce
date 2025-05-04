# JWT generation, hash and verify password, current user logic
from fastapi import Request, HTTPException, status, Depends
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
    return pwd_context.hash(password)


def verify_pwd(password: str, hashed_pwd):
    return pwd_context.verify(password, hashed_pwd)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def set_access_token(response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800,
    )


def get_current_user(request: Request, db: Session = Depends(get_db)):
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


def is_logged_in(request: Request):
    token = request.cookies.get("access_token")

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already logged in.",
                )
        except JWTError as e:
            return {"message": f"some error occured: {e}"}
