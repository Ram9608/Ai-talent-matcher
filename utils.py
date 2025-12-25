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
    try:
        # Sabse latest stable model use karein
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        
        prompt = f"Analyze this resume: {resume_text} against this JD: {jd}. Give match % and feedback."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Agar naya model bhi fail ho toh default 'gemini-pro' try karein
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            return "AI Error: Model limit reached or temporary down. Please try again after 1 minute."