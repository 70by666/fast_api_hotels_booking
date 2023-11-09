from datetime import date

from sqlalchemy import select, or_, and_, func

from src.bookings.models import Booking
from src.database import async_session_maker
from src.hotels.models import Hotel
from src.hotels.rooms.models import Room
from src.service.base import BaseService
from src.service.service import get_booked_rooms


class HotelService(BaseService):
    model = Hotel

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        booked_rooms = get_booked_rooms(date_from, date_to)

        booked_hotels = (
            select(Room.hotel_id, func.sum(
                Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
            ).label("rooms_left"))
            .select_from(Room)
            .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
            .group_by(Room.hotel_id)
            .cte("booked_hotels")
        )

        get_hotels_with_rooms = (
            select(
                Hotel.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotel.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotel.location.like(f"%{location}%"),
                )
            )
        )
        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
