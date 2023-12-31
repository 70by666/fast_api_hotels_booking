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


class RoomCannotBeBookedException(HotelsException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Не осталось свободных номеров'


class DateFromCannotBeAfterDateToException(HotelsException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Дата заезда не может быть позже даты выезда'


class CannotBookHotelForLongPeriodException(HotelsException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Невозможно забронировать отель сроком более месяца'
