from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotel.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    def __str__(self):
        return f'Номер {self.name}'
