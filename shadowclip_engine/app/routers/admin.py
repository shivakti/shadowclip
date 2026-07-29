from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..db import get_session
from ..models import User
from ..security import admin_required

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
def list_users(_: User = Depends(admin_required), session: Session = Depends(get_session)):
    return session.exec(select(User)).all()
