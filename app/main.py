# app/main.py

from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="SleepWise: Sleep Debt Tracker",
    description="Track your sleep debt and get AI-based recovery suggestions.",
    version="1.0.0"
)

# Mount API routes
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to SleepWise API!"}
