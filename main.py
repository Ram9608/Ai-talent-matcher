from fastapi import FastAPI, UploadFile, File, Form, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import shutil
import os

# Apni files ko import karna
from . import models, database, utils

# Database tables ko initial start par hi banana
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Talent Matcher Pro with Gemini")

# Templates folder ka setup
templates = Jinja2Templates(directory="templates")

# Data folder check karna
if not os.path.exists("data"):
    os.makedirs("data")

# Database session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. DASHBOARD (Frontend) ---
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- 2. UPLOAD & GEMINI ANALYSIS ---
@app.post("/upload/")
async def upload_resume(
    job_description: str = Form(...), 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # 1. File ko save karna
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. PDF se text nikalna aur Match Score (TF-IDF) nikalna
    resume_text = utils.extract_text_from_pdf(file_path)
    score = utils.calculate_match_score(resume_text, job_description)
    
    # 3. Gemini AI Feedback (Naya AI Logic)
    # Hum 'await' use kar rahe hain kyunki AI response mein thoda time lagta hai
    feedback = await utils.generate_llm_feedback(resume_text, job_description)
    
    # 4. Data ko SQL Database mein save karna
    new_candidate = models.Candidate(
        filename=file.filename,
        job_description=job_description,
        match_score=score,
        feedback=feedback
    )
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    
    return {
        "status": "Success", 
        "score": score, 
        "ai_feedback": feedback
    }

# --- 3. RANKINGS (DSA Sorting) ---
@app.get("/rankings/")
def get_rankings(db: Session = Depends(get_db)):
    # Database se high score wale candidates pehle dikhana
    candidates = db.query(models.Candidate).order_by(models.Candidate.match_score.desc()).all()
    return {"rankings": candidates}