from pwdlib import PasswordHash
import jwt 
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, timedelta, timezone

from core.config import settings
from core.database import get_db

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User

password_hash = PasswordHash((Argon2Hasher(),))

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def hash_password(plain_password : str) -> str : 
    return password_hash.hash(plain_password)

def verify_password(plain_password : str, hashed_password : str) -> bool : 
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(user_id : str) -> str :
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_time)
    payload = {
        "sub" : str(user_id),
        "exp" : expire
    }
    return jwt.encode(
        payload=payload,
        key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

def decode_access_token(token : str) -> str : 
    try : 
        return jwt.decode(
            token,
            key=settings.jwt_secret_key,
            algorithms=settings.jwt_algorithm
        )
    except jwt.InvalidTokenError :
        raise

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)) -> User :
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token=token)
    user_id = payload.get("sub")

    if not user_id :
        raise credentials_exception

    try : 
        user = db.query(User).filter(User.id == str(user_id)).first()

    except Exception:
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user