from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, String

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="USER")  # "ADMIN" o "USER"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    