from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    job_description = Column(String)
    match_score = Column(Float)
    feedback = Column(String)  # Ye line AI feedback store karegi