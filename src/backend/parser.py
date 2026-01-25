import pypdf
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import logging
from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS
from io import BytesIO
from calendar_logic import (
    json_to_calendar,
    send_to_calendar,
    get_authorization_url,
    exchange_code_for_credentials
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

genai.configure(api_key=api_key)

# Temporary storage for calendar events (keyed by OAuth state)
# In production, use Redis or a database
pending_events = {}


@app.route('/upload', methods=['POST'])
def upload():
    """Process PDF and store events, then redirect to Google OAuth"""
    uploaded_file = request.files['pdf_file']
    course_name = request.form.get('course_name')
    logger.info(f"=== UPLOAD START ===")
    logger.info(f"File: {uploaded_file.filename}, Course: {course_name}")

    # Extract text from uploaded PDF
    text = extract_text_from_upload(uploaded_file)
    logger.info(f"Extracted text length: {len(text)} chars")

    # Get assignments from Gemini API
    assignments_json = api(text)
    logger.info(f"Gemini response: {assignments_json}")

    # Convert to calendar events
    calendar_events = json_to_calendar(assignments_json, course_name)
    logger.info(f"Calendar events created: {len(calendar_events)}")
    logger.info(f"Events: {calendar_events}")

    # Get OAuth URL and state
    redirect_uri = url_for('oauth_callback', _external=True)
    authorization_url, state = get_authorization_url(redirect_uri)

    # Store events in server-side storage keyed by state
    pending_events[state] = calendar_events
    logger.info(f"Stored {len(calendar_events)} events with state: {state}")
    logger.info(f"Redirect URI: {redirect_uri}")
    logger.info(f"=== UPLOAD END ===")

    return jsonify({
        "message": f"Successfully processed {uploaded_file.filename}",
        "events_count": len(calendar_events),
        "auth_url": authorization_url
    })


@app.route('/callback')
def oauth_callback():
    """Handle OAuth callback from Google"""
    logger.info(f"=== CALLBACK START ===")
    code = request.args.get('code')
    state = request.args.get('state')
    logger.info(f"Received code: {code[:20]}..." if code else "No code received!")
    logger.info(f"Received state: {state}")

    redirect_uri = url_for('oauth_callback', _external=True)
    logger.info(f"Redirect URI: {redirect_uri}")

    # Exchange code for credentials
    credentials = exchange_code_for_credentials(code, redirect_uri)
    logger.info(f"Credentials obtained: {credentials.token[:20]}..." if credentials.token else "No token!")

    # Get stored events using state
    calendar_events = pending_events.get(state, [])
    logger.info(f"Events from storage: {len(calendar_events)}")
    logger.info(f"Pending events keys: {list(pending_events.keys())}")

    if not calendar_events:
        logger.error("No calendar events found for this state!")
        return redirect(f"{FRONTEND_URL}?error=no_events")

    # Convert credentials to dict for send_to_calendar
    credentials_dict = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': list(credentials.scopes)
    }

    # Send events to calendar
    logger.info(f"Sending {len(calendar_events)} events to calendar...")
    added_events = send_to_calendar(calendar_events, credentials_dict)
    logger.info(f"Added events: {added_events}")

    # Clean up stored events
    pending_events.pop(state, None)
    logger.info(f"=== CALLBACK END ===")

    return redirect(f"{FRONTEND_URL}?success=true&count={len(added_events)}")


def extract_text_from_upload(uploaded_file):
    """Extract text from uploaded PDF file object"""
    text = ""
    reader = pypdf.PdfReader(BytesIO(uploaded_file.read()))

    for page in reader.pages:
        page_text = page.extract_text()
        text += page_text + "\n"

    return text

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
    Only return Assignment name : dates in MM/DD/2025 format (EXAMPLE: Homework 9:Homework 09/03/2025) (If a date in the document mentions a month and day but lacks a year, assume the year is 2026.). 
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
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)