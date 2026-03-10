import uuid
from sqlalchemy import Column, String, Integer, DateTime
from app.db.database import Base
from datetime import datetime

class Call(Base):
    __tablename__ = "calls"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, index=True)
    caller_number = Column(String)
    status = Column(String, default="IN_PROGRESS")
    start_time = Column(DateTime, default=datetime.utcnow)

class Transcript(Base):
    __tablename__ = "transcripts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    call_id = Column(String, index=True)
    full_text = Column(String) 
    summary = Column(String)
