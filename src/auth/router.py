from fastapi import APIRouter, Response, Depends

from src.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from src.auth.auth import auth_user, create_access_token, create_user
from src.auth.dependencies import get_current_user, get_current_superuser
from src.auth.models import User
from src.auth.schemas import SUserAuth, SAuthRegisterLogout, SAuthLogin, SMe, SAllUsers
from src.auth.service import UserService

router = APIRouter(
    prefix='/auth',
    tags=['Auth and Users'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth) -> SAuthRegisterLogout:
    user = await create_user(user_data.email, user_data.password)
    if user:
        raise UserAlreadyExistsException()
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': None,
        'details': None,
    }


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth) -> SAuthLogin:
    user = await auth_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException()
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('hotels_access_token', access_token, httponly=True)
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': {'access_token': access_token},
        'details': None,
    }


@router.post('/logout')
async def logout_user(response: Response) -> SAuthRegisterLogout:
    response.delete_cookie('hotels_access_token')
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': None,
        'details': None,
    }


@router.get('/me')
def read_user_me(current_user: User = Depends(get_current_user)) -> SMe:
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': current_user,
        'details': None,
    }


@router.get('/all_users', dependencies=[Depends(get_current_superuser)])
async def get_all_users() -> SAllUsers:
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': await UserService.find_all(),
        'details': None,
    }
