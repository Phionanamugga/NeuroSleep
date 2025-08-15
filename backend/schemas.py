from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SleepCreate(BaseModel):
    start: datetime
    end: datetime
    notes: Optional[str] = None

class SleepOut(BaseModel):
    id: int
    user_id: int
    start: datetime
    end: datetime
    duration_hours: float
    notes: Optional[str] = None
    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility