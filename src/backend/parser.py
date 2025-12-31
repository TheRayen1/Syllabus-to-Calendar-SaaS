import pypdf
import google.generativeai as genai
from dotenv import load_dotenv
import os 
import json
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key="")

def parse():
    pdf_path = "test/"
    pdf_path += input("Enter syllabus Efile name: ")
    pdf_path += ".pdf"
    text= extract_text_pypdf(pdf_path)
    response = api(text)
    print(response)
    return response

def extract_text_pypdf(pdf_path):
    """Extract text from PDF using pypdf"""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        
        print(f"Number of pages: {len(reader.pages)}")
        
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            #text += f"\n--- Page {page_num} ---\n"
            text += page_text + "\n"
    
    return text
def api(text): 
    prompt = """
    You are a precise data extraction assistant. Your task is to find all my assignments + dates for this class. 
    Only return Assignment name : dates in MM/DD/2025 format (EXAMPLE: Homework 9:Homework 09/03/2025) (If a date in the document mentions a month and day but lacks a year, assume the year is 2025.). 
     If a due date is a range (e.g., "Oct 1-3"), use the final date of the range.

    Do not output anything else.
    IF DOCUMENT DOES NOT EXPLICITY STATE THE DATE, DO NOT RETURN IT.

."""

    model = genai.GenerativeModel("gemini-2.5-flash-lite")
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
    })#, indent=2

if __name__ == "__main__":
    parse()
