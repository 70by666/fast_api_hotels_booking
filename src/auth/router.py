from fastapi import APIRouter, HTTPException, status, Response

from src.auth.auth import auth_user, create_access_token, create_user
from src.auth.schemas import SUserAuth

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
            detail='Пользователь существует'
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
            detail='Неверная почта или пароль или пользователь не существует'
        )
    access_token = create_access_token({'sub': user.id})
    response.set_cookie('hotels_access_token', access_token, httponly=True)
    return {
        'status': 'success',
        'data': {'access_token': access_token},
        'details': None,
    }
