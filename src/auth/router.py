from fastapi import APIRouter, Response, Depends

from src.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
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
        raise UserAlreadyExistsException()
    return {
        'status': 'success',
        'data': None,
        'details': None,
    }


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await auth_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException()
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
    return {
        'status': 'success',
        'data': {
            'email': current_user.email,
            'id': current_user.id,
            'is_active': current_user.is_active,
            'is_superuser': current_user.is_superuser,
            'is_verified': current_user.is_verified,
            'created_at': current_user.created_at,
        },
        'details': None,
    }


@router.get('/all_users', dependencies=[Depends(get_current_superuser)])
async def get_all_users():
    return {
        'status': 'success',
        'data': await UserService.find_all(),
        'details': None,
    }
