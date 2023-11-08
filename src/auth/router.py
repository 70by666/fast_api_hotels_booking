from fastapi import APIRouter, HTTPException, status, Response, Depends

from src.auth.auth import auth_user, create_access_token, create_user
from src.auth.dependencies import get_current_user, get_current_superuser
from src.auth.models import User
from src.auth.schemas import SUserAuth
from src.auth.service import UserService

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    user = await create_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь уже существует',
        )
    return {
        'status': 'success',
        'data': None,
        'details': None,
    }


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await auth_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль или пользователь не существует',
        )
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('hotels_access_token', access_token, httponly=True)
    return {
        'status': 'success',
        'data': {'access_token': access_token},
        'details': None,
    }


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('hotels_access_token')
    return {
        'status': 'success',
        'data': None,
        'details': None,
    }


@router.get('/me')
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get('/all_users')
async def get_all_users(current_superuser: User = Depends(get_current_superuser)):
    return {
        'status': 'success',
        'data': await UserService.find_all(),
        'details': None,
    }
