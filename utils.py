import PyPDF2
import google.generativeai as genai
import os

# Gemini Config
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_text_from_pdf(file_file):
    try:
        pdf_reader = PyPDF2.PdfReader(file_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def get_gemini_response(resume_text, jd):
    # Multiple models try karega taaki 404 error na aaye
    models_to_try = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-flash-latest']
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = f"Analyze this resume: {resume_text} against this JD: {jd}. Give match % and feedback."
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            continue 
            
    return "AI Error: Gemini models are currently busy. Please try again in 1 minute."