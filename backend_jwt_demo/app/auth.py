from datetime import datetime, timedelta
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import Session
from .models import User
from .database import get_db

# JWT settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class UserRegister(BaseModel):
    username: str
    password: str
    role: str

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

@router.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = pwd_context.hash(user.password)
    new_user = User(username=user.username, password=hashed_pw, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "role": new_user.role}

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