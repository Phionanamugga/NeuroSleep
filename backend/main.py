# backend/main.py
from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List

app = FastAPI(title="Sleep Tracker Pro", version="1.0")

# Pydantic model for a sleep entry
class SleepEntry(BaseModel):
    date: str
    hours: float
    quality: str

# Temporary in-memory store
sleep_data: List[SleepEntry] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Sleep Tracker Pro API"}

@app.post("/sleep")
def add_sleep(entry: SleepEntry):
    sleep_data.append(entry)
    return {"message": "Sleep entry added successfully", "data": entry}

@app.get("/sleep")
def get_sleep():
    return sleep_data
