import pypdf
import google.generativeai as genai
from dotenv import load_dotenv
import os 
import json
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key="")

def main():
    pdf_path = "test/"
    pdf_path += input("Enter syllabus Efile name: ")
    pdf_path += ".pdf"
    course_name = input("Enter course name: ")
    text= extract_text_pypdf(pdf_path)
    response = api(text, course_name)
    print(response)

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
def api(text, course_name): 
    prompt= "find all my assignments + dates for this class. Only return Assignment name + dates in MM/DD/2025 format. Do not output anything else. IF DOCUMENT DOES NOT EXPLICITY STATE THE DATE, DO NOT RETURN ANYTHING"
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    text += prompt
    response = model.generate_content(text)
    # Convert response to JSON
    assignments = []
    lines = response.text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if ': ' in line:
            name, date = line.split(': ', 1)
            assignments.append({
                "assignment_name": name.strip(),
                "due_date": date.strip()
            })
    
    return json.dumps({
        "course": course_name,  
        "assignments": assignments
    }, indent=2)

if __name__ == "__main__":
    main()
