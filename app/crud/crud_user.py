from typing import Optional

from sqlalchemy.orm import Session
from starlette.config import Config
from jose import jwt

from app import models, schemas
from app.core.security import get_password_hash, verify_password

config = Config('.env')

def get_users_by_workspace(db: Session, workspace_id: int):
    return db.query(models.User).filter(models.User.workspace == workspace_id).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_access_token(db: Session, access_token: str):
    payload = jwt.decode(access_token, config.SECRET_KEY, algorithm=config.ALGORITHM)
    id: str = payload.get("sub")
    return get_user(db, id)

def create_user(db: Session, user_create: schemas.UserCreate):
    hashed_password = get_password_hash(user_create.password)
    db_user = models.User(
        email=user_create.email, 
        first_name=user_create.first_name, 
        last_name=user_create.last_name, 
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user