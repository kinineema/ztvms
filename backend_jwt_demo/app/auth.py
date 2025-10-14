from datetime import datetime, timedelta
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET = "change-me"
ALGO = "HS256"
ACCESS_MIN = 15
REFRESH_DAYS = 7

USERS = {
    "admin@demo":   {"password": "admin",   "role": "admin"},
    "analyst@demo": {"password": "analyst", "role": "analyst"},
    "viewer@demo":  {"password": "viewer",  "role": "viewer"},
}

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    role: Literal["admin","analyst","viewer"]
    token_type: str = "bearer"

def create_access(sub: str, role: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_MIN)
    return jwt.encode({"sub": sub, "role": role, "exp": exp}, SECRET, algorithm=ALGO)

def create_refresh(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(days=REFRESH_DAYS)
    return jwt.encode({"sub": sub, "type": "refresh", "exp": exp}, SECRET, algorithm=ALGO)

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    email = form.username
    pw = form.password
    user = USERS.get(email)
    if not user or user["password"] != pw:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    role = user["role"]
    return {
        "access_token": create_access(email, role),
        "refresh_token": create_refresh(email),
        "role": role,
    }

class RefreshIn(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=TokenOut)
def refresh(body: RefreshIn):
    try:
        decoded = jwt.decode(body.refresh_token, SECRET, algorithms=[ALGO])
        if decoded.get("type") != "refresh":
            raise ValueError("not refresh")
        email = decoded["sub"]
        role = USERS[email]["role"]
        return {
            "access_token": create_access(email, role),
            "refresh_token": create_refresh(email),
            "role": role,
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
