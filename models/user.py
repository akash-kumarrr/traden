from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base

from typing import TYPE_CHECKING, List


class User(Base):
    __tablename__= "users"
    name : Mapped[str] = mapped_column(String)
    email : Mapped[str] = mapped_column(String)
    password : Mapped[str] = mapped_column(String)