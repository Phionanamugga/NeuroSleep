from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from . import crud, schemas, deps
from .database import engine, Base
import os

app = FastAPI(title='Sleep Tracker Pro')

# create tables (for demo; in prod use migrations)
Base.metadata.create_all(bind=engine)

# simple CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {'msg': 'Sleep Tracker Pro — API is running'}

# auth endpoints
@app.post('/auth/register', response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate):
    user = crud.get_user_by_username(user_in.username)
    if user:
        raise HTTPException(status_code=400, detail='username already exists')
    created = crud.create_user(user_in)
    return created

@app.post('/auth/login', response_model=schemas.Token)
def login(form_data: schemas.UserLogin):
    token = crud.authenticate_user_and_get_token(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail='invalid credentials')
    return {'access_token': token, 'token_type': 'bearer'}

# protected endpoints
@app.post('/sleeps', response_model=schemas.SleepOut)
def add_sleep(entry: schemas.SleepCreate, current_user=Depends(deps.get_current_user)):
    return crud.create_sleep(current_user.id, entry)

@app.get('/sleeps', response_model=list[schemas.SleepOut])
def list_sleeps(current_user=Depends(deps.get_current_user)):
    return crud.get_sleeps_for_user(current_user.id)

@app.get('/sleeps/stats')
def stats(current_user=Depends(deps.get_current_user)):
    return crud.compute_stats(current_user.id)

@app.get('/export/csv')
def export_csv(current_user=Depends(deps.get_current_user)):
    from fastapi.responses import StreamingResponse
    import io, csv
    sleeps = crud.get_sleeps_for_user(current_user.id)
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['id','start','end','duration_hours','notes'])
    for s in sleeps:
        writer.writerow([s.id, s.start.isoformat(), s.end.isoformat(), round(s.duration_hours,2), s.notes or ''])
    si.seek(0)
    return StreamingResponse(iter([si.getvalue()]), media_type='text/csv', headers={'Content-Disposition':'attachment; filename="sleep_export.csv"'})

# static frontend
from fastapi.staticfiles import StaticFiles
app.mount('/app', StaticFiles(directory='frontend', html=True), name='frontend')

