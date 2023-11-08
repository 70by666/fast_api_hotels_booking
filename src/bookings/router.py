from typing import Optional

from fastapi import APIRouter

from src.bookings.schemas import SBooking
from src.bookings.service import BookingService

router = APIRouter(
    prefix='/bookings',
    tags=['bookings'],
)


@router.get('')
async def get_bookings() -> list[SBooking]:
    return await BookingService.find_all()
