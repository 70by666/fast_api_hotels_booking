from sqlalchemy import Column, Integer, DateTime, Boolean, String

from src.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
    is_verified = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
