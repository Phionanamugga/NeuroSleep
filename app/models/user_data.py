from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sleep_goal = Column(Float, default=8.0)  # desired sleep in hours
    timezone = Column(String, default="UTC")
    preferred_wake_time = Column(String, default="07:00")  # format HH:MM
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship (assuming a 'User' model exists)
    user = relationship("User", back_populates="user_data")
