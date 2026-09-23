from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import UserCreate, UserResponse

from core.database import get_db
from core.security import verify_password, create_access_token

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.user import User

from deps.user import create_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register")
async def register(user : UserCreate, db : Session = Depends(get_db)) :
    return create_user(user=user, db=db)


@router.post("/login")
async def login(creadentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    stmt = select(User).where(User.email == creadentials.username)
    user = db.execute(stmt).scalar_one_or_none()

    if not user or not verify_password(creadentials.password, user.password) :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exists."
        )

    access_token = create_access_token(str(user.id))

    return {
        "access_token" : access_token,
        "token_bearer" : "bearer"
    }