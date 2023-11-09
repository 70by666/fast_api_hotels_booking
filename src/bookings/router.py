from datetime import date

from fastapi import APIRouter, Depends

from src.exceptions import RoomCannotBeBookedException
from src.auth.dependencies import get_current_user
from src.bookings.schemas import SBookingResult
from src.bookings.service import BookingService
from src.auth.models import User

router = APIRouter(
    prefix='/bookings',
    tags=['bookings'],
)


@router.get('')
async def get_bookings(current_user: User = Depends(get_current_user)) -> SBookingResult:
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': await BookingService.find_all(id=current_user.id),
        'details': None,
    }


@router.post('')
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    current_user: User = Depends(get_current_user),
):
    booking = await BookingService.add(current_user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException()
