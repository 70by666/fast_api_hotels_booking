from fastapi import APIRouter

from src.bookings.schemas import SBookingResponse
from src.bookings.service import BookingService

router = APIRouter(
    prefix='/bookings',
    tags=['bookings'],
)


@router.get('')
async def get_bookings() -> SBookingResponse:
    return {
        'status': 'success',
        'data': await BookingService.find_all(),
        'details': None,
    }
