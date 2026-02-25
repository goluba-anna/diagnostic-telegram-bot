from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    DateTime,
    Date,
    Time,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class WorkingDay(Base):
    __tablename__ = "working_days"

    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True)
    start_time = Column(Time)
    end_time = Column(Time)
    is_active = Column(Boolean, default=True)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    start_time = Column(Time)
    duration_minutes = Column(Integer)
    status = Column(String, default="pending")  # pending, paid, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tariff = Column(String)
    amount = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)


class DiagnosticAnswer(Base):
    __tablename__ = "diagnostic_answers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
