from src.bookings.models import Booking
from src.service.base import BaseService


class BookingService(BaseService):
    model = Booking
