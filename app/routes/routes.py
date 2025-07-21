# app/api/routes.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

router = APIRouter()

class SleepInput(BaseModel):
    date: str = Field(..., example="2025-07-08")
    sleep_time: str = Field(..., example="22:30")  # 10:30 PM
    wake_time: str = Field(..., example="06:30")   # 6:30 AM
    recommended_sleep: float = Field(8.0, example=8.0)  # default to 8 hours

class SleepResponse(BaseModel):
    sleep_duration: float
    sleep_debt: float
    message: str

def calculate_sleep_duration(sleep_time: str, wake_time: str) -> float:
    """
    Calculate the number of hours slept.
    Handles overnight sleep (e.g., 23:00 to 06:00).
    """
    fmt = "%H:%M"
    sleep_dt = datetime.strptime(sleep_time, fmt)
    wake_dt = datetime.strptime(wake_time, fmt)

    if wake_dt <= sleep_dt:
        wake_dt += timedelta(days=1)

    duration = (wake_dt - sleep_dt).total_seconds() / 3600
    return round(duration, 2)

@router.post("/sleep", response_model=SleepResponse)
def track_sleep(data: SleepInput):
    duration = calculate_sleep_duration(data.sleep_time, data.wake_time)
    sleep_debt = round(data.recommended_sleep - duration, 2)
    
    msg = "Great! You met your sleep goal." if sleep_debt <= 0 else "You're in sleep debt. Try to rest more."

    return SleepResponse(
        sleep_duration=duration,
        sleep_debt=max(sleep_debt, 0),
        message=msg
    )
