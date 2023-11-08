from datetime import date
from typing import Optional

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int


class SBookingResult(BaseModel):
    status: str
    data: list[SBooking]
    details: Optional[str]
