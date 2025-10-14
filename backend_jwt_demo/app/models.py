from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, nullable=False)
    status = Column(String, default="queued")
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    findings = relationship("Finding", back_populates="scan")

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, index=True)
    tool = Column(String)
    name = Column(String)
    risk = Column(String)
    url = Column(String)
    param = Column(String)
    evidence = Column(Text)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    scan = relationship("Scan", back_populates="findings")