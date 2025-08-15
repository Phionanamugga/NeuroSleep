from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from . import crud, schemas, deps
from .database import engine, Base, get_db
import csv
import io
import os

# Initialize FastAPI app
app = FastAPI(title="Sleep Tracker Pro")

# Create database tables (for development; use Alembic migrations in production)
Base.metadata.create_all(bind=engine)

# Configure CORS for local development (restrict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API prefix for all endpoints
API_PREFIX = "/api"

# Frontend setup
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend index.html"""
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    with open(index_path) as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Authentication endpoints
@app.post(f"{API_PREFIX}/auth/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db=Depends(get_db)):
    """Register a new user."""
    try:
        user = crud.get_user_by_username(db, user_in.username)
        if user:
            raise HTTPException(status_code=400, detail="Username already exists")
        created = crud.create_user(db, user_in)
        return created
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@app.post(f"{API_PREFIX}/auth/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db=Depends(get_db)):
    """Authenticate user and return JWT token."""
    try:
        token = crud.authenticate_user_and_get_token(db, form_data.username, form_data.password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during authentication: {str(e)}")

# Protected sleep tracking endpoints
@app.post(f"{API_PREFIX}/sleeps", response_model=schemas.SleepOut)
def add_sleep(entry: schemas.SleepCreate, current_user=Depends(deps.get_current_user), db=Depends(get_db)):
    """Add a new sleep entry for the authenticated user."""
    try:
        return crud.create_sleep(db, current_user.id, entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating sleep entry: {str(e)}")

@app.get(f"{API_PREFIX}/sleeps", response_model=list[schemas.SleepOut])
def list_sleeps(current_user=Depends(deps.get_current_user), db=Depends(get_db)):
    """List all sleep entries for the authenticated user."""
    try:
        return crud.get_sleeps_for_user(db, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sleep entries: {str(e)}")

@app.get(f"{API_PREFIX}/sleeps/stats")
def stats(current_user=Depends(deps.get_current_user), db=Depends(get_db)):
    """Compute sleep statistics for the authenticated user."""
    try:
        return crud.compute_stats(db, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing stats: {str(e)}")

@app.get(f"{API_PREFIX}/export/csv")
def export_csv(current_user=Depends(deps.get_current_user), db=Depends(get_db)):
    """Export sleep entries as a CSV file."""
    try:
        sleeps = crud.get_sleeps_for_user(db, current_user.id)
        si = io.StringIO()
        writer = csv.writer(si)
        writer.writerow(["id", "start", "end", "duration_hours", "notes"])
        for s in sleeps:
            writer.writerow([s.id, s.start.isoformat(), s.end.isoformat(), round(s.duration_hours, 2), s.notes or ""])
        si.seek(0)
        return StreamingResponse(
            iter([si.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="sleep_export.csv"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting CSV: {str(e)}")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Mount static files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Redirect all unmatched paths to frontend
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    """Catch-all route to serve frontend for client-side routing"""
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    with open(index_path) as f:
        return HTMLResponse(content=f.read(), status_code=200)
    