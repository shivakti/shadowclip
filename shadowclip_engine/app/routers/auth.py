from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from ..db import get_session
from ..models import User
from ..security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: RegisterIn, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = User(email=data.email, password_hash=hash_password(data.password))

    # El PRIMER usuario que se registre será ADMIN automáticamente
    if session.exec(select(User)).first() is None:
        user.role = "ADMIN"

    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_token({"sub": user.id})
    return {"access_token": token, "user": {"id": user.id, "email": user.email, "role": user.role}}

@router.post("/login")
def login(data: LoginIn, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token = create_token({"sub": user.id})
    return {"access_token": token, "user": {"id": user.id, "email": user.email, "role": user.role}}
