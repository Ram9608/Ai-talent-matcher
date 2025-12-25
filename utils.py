import PyPDF2
import google.generativeai as genai
import os

# Gemini Config: Ye Render ki environment settings se key uthayega
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_text_from_pdf(file_file):
    """PDF file se text nikalne ke liye function"""
    try:
        # Direct file stream se read karega
        pdf_reader = PyPDF2.PdfReader(file_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def get_gemini_response(resume_text, jd):
    """AI model ko prompt bhej kar response lene ke liye"""
    try:
        # Model naam 'gemini-pro' use kar rahe hain taaki 404 error na aaye
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You are an expert HR Manager. Analyze the following resume against the job description.
        Resume: {resume_text}
        JD: {jd}
        
        Provide:
        1. Match Percentage
        2. Missing Keywords
        3. Final Verdict
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"