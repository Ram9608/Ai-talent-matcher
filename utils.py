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
        # Model ka naam bina 'models/' ke likhein, ye version sabse stable hai
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"Analyze this resume: {resume_text} against this JD: {jd}. Give match % and feedback."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"