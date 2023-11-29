from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as, TypeAdapter

from src.exceptions import RoomCannotBeBookedException
from src.auth.dependencies import get_current_user
from src.bookings.schemas import SBookingResult, SBookingResultAdd, SBookingDelete, SBooking
from src.bookings.service import BookingService
from src.auth.models import User
from src.tasks._email import create_booking_message
from src.tasks.tasks import send_booking_email

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('')
async def get_bookings(current_user: User = Depends(get_current_user)) -> SBookingResult:
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': await BookingService.find_all(user_id=current_user.id),
        'details': None,
    }


@router.post('')
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    current_user: User = Depends(get_current_user),
) -> SBookingResultAdd:
    booking = await BookingService.add(current_user.id, room_id, date_from, date_to)
    ta = TypeAdapter(SBooking)
    booking_dict = ta.dump_python(booking)
    send_booking_email.delay(booking_dict, current_user.email)
    if not booking:
        raise RoomCannotBeBookedException()
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': booking,
        'details': None,
    }


@router.delete('/{booking_id}')
async def del_booking(booking_id: int, current_user: User = Depends(get_current_user)) -> SBookingDelete:
    result = await BookingService.delete_booking_by_id(booking_id, current_user.id)
    if result:
        # noinspection PyTypeChecker
        return {
            'status': 'success',
            'data': None,
            'details': f'Удалена бронь под номером {booking_id}',
        }
    # noinspection PyTypeChecker
    return {
        'status': 'error',
        'data': None,
        'details': 'Вы не можете удалить не свою бронь',
    }
