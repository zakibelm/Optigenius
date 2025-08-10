import datetime as dt
from typing import Optional
from fastapi import FastAPI, Response, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .db import get_db
from . import repo

app = FastAPI(title="OptiGenius Starter", version="0.2.0")

class AppointmentIn(BaseModel):
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    datetime: str
    notes: Optional[str] = None

class AppointmentOut(BaseModel):
    status: str
    received: AppointmentIn

@app.get("/health")
def health():
    return {"ok": True}

@app.head("/health")
async def health_head():
    return Response(status_code=200)

@app.post("/appointments", response_model=AppointmentOut)
def create_appointment(payload: AppointmentIn, db: Session = Depends(get_db)):
    # Validation ISO 8601 simple
    try:
        dt.datetime.fromisoformat(payload.datetime.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid datetime format")

    # Persistance en base
    repo.create_appointment(db, payload)
    return {"status": "ok", "received": payload}
