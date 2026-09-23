from schemas.user import UserCreate, UserResponse
from models.user import User
from core.security import hash_password

from fastapi import HTTPException, status


from sqlalchemy.orm import Session
from sqlalchemy import select

def create_user(user : UserCreate, db : Session):
    user.password = hash_password(user.password)
    stmt = select(User).where(User.email == user.email)
    existing_user = db.scalars(stmt).first()

    if existing_user : 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            deatil="User already exists."
        )

    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user