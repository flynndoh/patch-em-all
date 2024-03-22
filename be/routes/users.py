from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy import func
from sqlmodel import select, Session

from database import get_session
from models import User

users_router = APIRouter(tags=["users"], prefix="/users")


@users_router.get("")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@users_router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.post("")
def create_user(user_name: str, user_email: EmailStr, session: Session = Depends(get_session)):
    if session.exec(select(func.count(User.id)).where(User.email == user_email)).one():
        raise HTTPException(status_code=400, detail="Email has already been registered")
    user = User(name=user_name, email=user_email, created=datetime.utcnow())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@users_router.put("/{user_id}")
def update_user(user_id: int, user_name: str | None = None, user_email: EmailStr | None = None, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if session.exec(select(func.count(User.id)).where(User.email == user_email)).one():
        raise HTTPException(status_code=400, detail="Email has already been registered")

    if user_name is not None:
        db_user.name = user_name
    if user_email is not None:
        db_user.email = user_email
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@users_router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}


