from datetime import date
from typing import List, Optional

from fastapi import APIRouter

from src.exceptions import DateFromCannotBeAfterDateToException, CannotBookHotelForLongPeriodException
from src.hotels.service import HotelService
from src.hotels.schemas import SHotelInfo, SHotel

router = APIRouter(
    prefix="/hotels",
    tags=['Hotels'],
)


@router.get("/{location}")
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date,
    date_to: date,
) -> List[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateToException()
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriodException()
    hotels = await HotelService.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SHotel]:
    result = await HotelService.find_one_or_none(id=hotel_id)
    return result
