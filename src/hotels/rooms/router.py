from datetime import date
from typing import List

from fastapi import APIRouter

from src.hotels.rooms.schemas import SRoomInfo
from src.hotels.rooms.service import RoomService

router = APIRouter(
    prefix="/hotels",
    tags=['Hotels'],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> List[SRoomInfo]:
    rooms = await RoomService.find_all(hotel_id, date_from, date_to)
    return rooms
