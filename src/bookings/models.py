from sqlalchemy import Column, Integer, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship

from src.database import Base


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_days = Column(Integer, Computed('date_to-date_from'))
    total_cost = Column(Integer, Computed('(date_to-date_from) * price'))

    def __str__(self):
        return f'Booking #{self.id}'
