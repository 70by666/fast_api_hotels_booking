from sqlalchemy import select, and_, or_, func

from src.bookings.models import Booking


def get_booked_rooms(date_from, date_to):
    booked_rooms = (
        select(Booking.room_id, func.count(Booking.room_id).label("rooms_booked"))
        .select_from(Booking)
        .where(
            or_(
                and_(
                    Booking.date_from >= date_from,
                    Booking.date_from <= date_to,
                ),
                and_(
                    Booking.date_from <= date_from,
                    Booking.date_to > date_from,
                ),
            ),
        )
        .group_by(Booking.room_id)
        .cte("booked_rooms")
    )
    return booked_rooms
