import google.generativeai as genai
import fitz  # PyMuPDF
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Google Gemini Configuration
# Google AI Studio (aistudio.google.com) se apni key yahan dalein
genai.configure(api_key="AIzaSyDjgoumPgpogxFhlgFIHkjsYGnPut5cfck")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. PDF se text nikalne ka function
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 3. Math logic: TF-IDF se match score nikalna
def calculate_match_score(resume_text, job_description):
    if not resume_text.strip() or not job_description.strip():
        return 0.0
    
    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Cosine Similarity nikalna
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(score[0][0] * 100, 2)

# 4. Gemini AI Logic: Resume aur JD compare karke feedback dena
async def generate_llm_feedback(resume_text, job_desc):
    # Prompt ko chota rakha hai taaki response fast aaye
    prompt = f"""
    You are a professional HR recruiter. 
    Analyze the following resume against the job description.
    
    Resume (First 1500 chars): {resume_text[:1500]}
    Job Description: {job_desc}
    
    Task: Give 2 short sentences of feedback. 
    1. Why it matches or why not.
    2. One tip for improvement.
    Keep it under 50 words.
    """
    
    try:
        # Gemini API call (Asynchronous)
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Manual review required. The score has been calculated based on keywords."
