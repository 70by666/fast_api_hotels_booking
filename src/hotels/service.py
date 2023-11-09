from sqlalchemy import delete

from src.database import async_session_maker
from src.hotels.models import Hotel
from src.service.base import BaseService


class HotelService(BaseService):
    model = Hotel
