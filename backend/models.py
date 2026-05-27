from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    organization = Column(String(300))
    country = Column(String(200))
    deadline = Column(String(100))
    eligibility = Column(Text)
    funding_amount = Column(String(200))
    category = Column(String(100))
    link = Column(String(1000), unique=True)
    description = Column(Text)
    tags = Column(String(500))
    is_remote = Column(Boolean, default=False)
    women_friendly = Column(Boolean, default=False)
    indian_eligible = Column(Boolean, default=False)
    student_eligible = Column(Boolean, default=False)
    age_min = Column(Integer, nullable=True)
    age_max = Column(Integer, nullable=True)
    application_fee = Column(String(100))
    source_url = Column(String(1000))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ApplicationTracker(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, nullable=False)
    status = Column(String(50), default="saved")
    notes = Column(Text)
    priority = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)