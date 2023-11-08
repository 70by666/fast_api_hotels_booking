from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from src.auth.service import UserService
from src.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_AUTH, settings.ALGORITHM)
    return encoded_jwt


async def create_user(email: EmailStr, password: str):
    existing_user = await UserService.find_one_or_none(email=email)
    if existing_user:
        return None
    hashed_password = get_password_hash(password)
    await UserService.add(
        email=email,
        password=hashed_password,
        is_active=True,
        is_superuser=False,
        is_verified=False,
        created_at=datetime.utcnow(),
    )
    return True


async def auth_user(email: EmailStr, password: str):
    user = await UserService.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user
