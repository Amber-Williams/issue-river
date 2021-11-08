from datetime import datetime, timedelta
from typing import Any, Union
from os.path import join, dirname
import os

from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv, find_dotenv

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
# 60 minutes * 24 hours * 7 days = 7 days
ACCESS_TOKEN_EXPIRY: int = 60 * 24 * 7


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRY
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)