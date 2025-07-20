# app/db/models.py

from sqlalchemy import Column, Integer, String, Float, Date
from app.db.database import Base

class SleepLog(Base):
    __tablename__ = "sleep_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    sleep_time = Column(String)
    wake_time = Column(String)
    sleep_duration = Column(Float)
