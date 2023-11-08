from fastapi import HTTPException, status


class HotelsException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(HotelsException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует'


class IncorrectEmailOrPasswordException(HotelsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверная почта или пароль'


class TokenDoesNotExistException(HotelsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен не существует'


class InvalidTokenException(HotelsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Некорректный токен'


class TokenExpiredException(HotelsException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истек'
