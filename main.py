from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
import models, database, utils
from database import engine
from fastapi.responses import HTMLResponse

app = FastAPI()

# Database setup
models.Base.metadata.create_all(bind=engine)

# Sahi templates folder link kiya gaya hai
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/match", response_class=HTMLResponse)
async def match_resume(request: Request, jd: str = Form(...), file: UploadFile = File(...)):
    try:
        # Resume se text nikalna
        resume_text = utils.extract_text_from_pdf(file.file)
        # Gemini AI se response lena
        result = utils.get_gemini_response(resume_text, jd)
        
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": result,
            "jd": jd
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": f"Error: {str(e)}",
            "jd": jd
        })