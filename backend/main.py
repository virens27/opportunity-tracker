from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db, create_tables
from models import Opportunity, ApplicationTracker
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Opportunity Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()

# --- Schemas ---
class OpportunityOut(BaseModel):
    id: int
    title: str
    organization: Optional[str]
    country: Optional[str]
    deadline: Optional[str]
    category: Optional[str]
    funding_amount: Optional[str]
    link: Optional[str]
    description: Optional[str]
    tags: Optional[str]
    women_friendly: bool
    indian_eligible: bool
    student_eligible: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TrackerIn(BaseModel):
    opportunity_id: int
    status: str = "saved"
    notes: Optional[str] = None
    priority: int = 1

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Opportunity Tracker API is running!"}

@app.get("/opportunities", response_model=List[OpportunityOut])
def get_opportunities(
    search: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    women_friendly: Optional[bool] = None,
    indian_eligible: Optional[bool] = None,
    student_eligible: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Opportunity).filter(Opportunity.is_active == True)

    if search:
        query = query.filter(
            Opportunity.title.ilike(f"%{search}%") |
            Opportunity.description.ilike(f"%{search}%") |
            Opportunity.tags.ilike(f"%{search}%")
        )
    if category:
        query = query.filter(Opportunity.category.ilike(f"%{category}%"))
    if country:
        query = query.filter(Opportunity.country.ilike(f"%{country}%"))
    if women_friendly is not None:
        query = query.filter(Opportunity.women_friendly == women_friendly)
    if indian_eligible is not None:
        query = query.filter(Opportunity.indian_eligible == indian_eligible)
    if student_eligible is not None:
        query = query.filter(Opportunity.student_eligible == student_eligible)

    return query.offset(skip).limit(limit).all()

@app.get("/opportunities/{opp_id}", response_model=OpportunityOut)
def get_opportunity(opp_id: int, db: Session = Depends(get_db)):
    opp = db.query(Opportunity).filter(Opportunity.id == opp_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp

@app.post("/track")
def track_application(data: TrackerIn, db: Session = Depends(get_db)):
    tracker = ApplicationTracker(**data.dict())
    db.add(tracker)
    db.commit()
    db.refresh(tracker)
    return tracker

@app.get("/track")
def get_tracked(db: Session = Depends(get_db)):
    return db.query(ApplicationTracker).all()

@app.put("/track/{track_id}")
def update_tracker(track_id: int, data: TrackerIn, db: Session = Depends(get_db)):
    item = db.query(ApplicationTracker).filter(ApplicationTracker.id == track_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in data.dict().items():
        setattr(item, key, value)
    db.commit()
    return item

@app.post("/admin/seed")
def seed_database(db: Session = Depends(get_db)):
    from scraper import run_scraper
    try:
        run_scraper()
        count = db.query(Opportunity).count()
        return {"message": f"Seeding complete! {count} opportunities in database."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin/count")
def count_opportunities(db: Session = Depends(get_db)):
    count = db.query(Opportunity).count()
    return {"total_opportunities": count}