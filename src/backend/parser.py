import pypdf
import google.generativeai as genai
from dotenv import load_dotenv
import os 
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import calendar_logic 



app = Flask(__name__)
CORS(app)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
@app.route('/upload', methods= ['POST'])
def test_upload():
    uploaded_file = request.files['pdf_file']
    course_name = request.form.get('course_name')
    response= parse(uploaded_file)
    data = json.loads(response)
    data['course_name'] = course_name
    calendar_ready = calendar_logic.json_to_calendar(response, course_name)

    calendar_logic.send_to_calendar(calendar_ready)

    return jsonify({"status": "Success"})

def parse(pdf_path):
    text= extract_text_pypdf(pdf_path)
    response = api(text)
    #print(response)
    return response

def extract_text_pypdf(pdf_path):
    """Extract text from PDF using pypdf"""
    text = ""
    reader = pypdf.PdfReader(pdf_path)

    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    return text
def api(text): 
    prompt = """
    You are a precise data extraction assistant. Your task is to find all my assignments + dates for this class. 
    Only return Assignment name : dates in MM/DD/2025 format (EXAMPLE: Homework 9:Homework 09/03/2025) (If a date in the document mentions a month and day but lacks a year, assume the year is 2025.). 
     If a due date is a range (e.g., "Oct 1-3"), use the final date of the range.

    Do not output anything else.
    IF DOCUMENT DOES NOT EXPLICITY STATE THE DATE, DO NOT RETURN IT.

."""

    model = genai.GenerativeModel("gemini-1.5-flash")
    text += prompt
    response = model.generate_content(text)
    # Convert response to JSON
    assignments = []
    lines = response.text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if ': ' in line or ' - ' in line:
            separator = ': ' if ': ' in line else ' - '
            name, date = line.split(separator, 1)
            assignments.append({
                "assignment_name": name.strip(),
                "due_date": date.strip()
            })
    #print("Raw Gemini:", response.text)
    return json.dumps({
#        "course": course_name,  
        "assignments": assignments
    })

if __name__ == "__main__":
    app.run(port=5000)
