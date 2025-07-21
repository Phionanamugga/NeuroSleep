from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import SleepLog
from datetime import date
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Pydantic schemas
class SleepLogCreate(BaseModel):
    date: date
    sleep_time: str
    wake_time: str
    sleep_duration: float

class SleepLogOut(SleepLogCreate):
    id: int

    class Config:
        orm_mode = True

# Endpoint to create sleep log
@router.post("/sleep", response_model=SleepLogOut)
def create_sleep_log(entry: SleepLogCreate, db: Session = Depends(get_db)):
    db_entry = SleepLog(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# Endpoint to get all sleep logs
@router.get("/sleep", response_model=List[SleepLogOut])
def read_sleep_logs(db: Session = Depends(get_db)):
    return db.query(SleepLog).order_by(SleepLog.date.desc()).all()

