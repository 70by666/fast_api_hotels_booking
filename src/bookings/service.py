from datetime import date

from sqlalchemy import select, and_, or_, func, insert, delete

from src.bookings.models import Booking
from src.database import engine, async_session_maker
from src.hotels.rooms.models import Room
from src.service.base import BaseService


class BookingService(BaseService):
    model = Booking

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Booking).where(
                and_(
                    Booking.room_id == room_id,
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_from <= date_to,
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to > date_from,
                        ),
                    )
                )
            ).cte('booked_rooms')

            get_rooms_left = select(
                (Room.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
                ).select_from(Room).join(
                    booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True
                ).where(Room.id == room_id).group_by(
                    Room.quantity, booked_rooms.c.room_id
                )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Room.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_booking = insert(Booking).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Booking)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def delete_booking_by_id(cls, booking_id, user_id):
        async with async_session_maker() as session:
            booking = await cls.find_by_id(booking_id)
            if not booking:
                return None
            if not booking.user_id == user_id:
                return None
            query = delete(cls.model).where(cls.model.id == booking_id)
            await session.execute(query)
            await session.commit()
            return booking_id
