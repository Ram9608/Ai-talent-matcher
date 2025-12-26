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
        return f"Error: {str(e)}"

def get_gemini_response(resume_text, jd):
    try:
        # Latest stable model for free tier
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analyze this resume: {resume_text} against this JD: {jd}. Provide match % and feedback."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"