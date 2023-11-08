from datetime import datetime

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from exceptions import InvalidTokenException, TokenDoesNotExistException, TokenExpiredException
from src.auth.models import User
from src.auth.service import UserService
from src.config import settings


def get_token(request: Request):
    token = request.cookies.get('hotels_access_token')
    if not token:
        raise TokenDoesNotExistException()
    return token


async def get_current_user(access_token: str = Depends(get_token)):
    try:
        payload = jwt.decode(access_token, settings.SECRET_AUTH, settings.ALGORITHM)
    except JWTError:
        raise InvalidTokenException()
    expire = payload.get('exp')
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException()
    user_id = payload.get('sub')
    if not user_id:
        raise InvalidTokenException()
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise InvalidTokenException()

    return user


async def get_current_superuser(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
    return current_user
