# from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException

from database import models
from schemas import users
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.users).filter(models.users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.users).filter(models.users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.users).offset(skip).limit(limit).all()


def create_user(db: Session, user: users.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    try:
        db_user = models.users(
            email=user.email,
            hashed_password=hashed_password,
            is_active=True,
            id_empresa=1,
        )
        db.add(db_user)
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=401, detail=f"Sorry, that username already exists."
        )

    db.commit()
    db.refresh(db_user)
    return db_user
