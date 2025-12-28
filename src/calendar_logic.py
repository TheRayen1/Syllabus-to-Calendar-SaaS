import parser
import json 
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/calendar']

def json_to_calendar(output):
    course_name = input("Please enter Course Name: ")
    data = json.loads(output)
    calendar_events = []
    
    for assignment in data["assignments"]:
        # Convert MM/DD/YYYY to YYYY-MM-DD
        due_date = assignment["due_date"]
        year = due_date.split('/')[2]
        month = due_date.split('/')[0]
        day = due_date.split('/')[1]
        iso_date = f"{year}-{month}-{day}"
        
        event = {
            "summary": f"{course_name}: {assignment['assignment_name']}",
            "start": {
                "dateTime": f"{iso_date}T23:00:00",  # 5 PM default
                "timeZone": "America/New_York"
            },
            "end": {
                "dateTime": f"{iso_date}T23:59:00",  # 1 hour duration
                "timeZone": "America/New_York"
            }
        }
        calendar_events.append(event)
    calendar_ready = json.dumps(calendar_events, indent=2)
    return calendar_ready

def send_to_calendar(calendar_ready):
    # Convert JSON string to Python list
    events = json.loads(calendar_ready)
    
    # Authenticate
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Build service
    service = build('calendar', 'v3', credentials=creds)
    
    # Insert each event
    for event in events:
        service.events().insert(calendarId='primary', body=event).execute()
        print(f"Added: {event['summary']}")
    
    return "Done"
output = parser.parse()
calendar_ready = json_to_calendar(output)

send_to_calendar(calendar_ready)
