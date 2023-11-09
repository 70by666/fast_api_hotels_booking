from datetime import date

from sqlalchemy import func, select, and_, or_

from src.bookings.models import Booking
from src.database import async_session_maker
from src.hotels.rooms.models import Room
from src.service.base import BaseService
from src.service.service import get_booked_rooms


class RoomService(BaseService):
    model = Room

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        booked_rooms = get_booked_rooms(date_from, date_to)

        get_rooms = (
            select(
                Room.__table__.columns,
                (Room.price * (date_to - date_from).days).label("total_cost"),
                (Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left"),
            )
            .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
            .where(
                Room.hotel_id == hotel_id
            )
        )
        async with async_session_maker() as session:
            rooms = await session.execute(get_rooms)
            return rooms.mappings().all()
