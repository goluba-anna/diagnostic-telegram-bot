from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String, nullable=True)

    bookings = relationship("Booking", back_populates="user")


class WorkingDay(Base):
    __tablename__ = "working_days"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
