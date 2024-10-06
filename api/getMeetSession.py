# [START calendar_quickstart]
from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random
import string
from datetime import datetime, timedelta

def get_file_path(file_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, file_name)


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def generate_random_string():
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(6))
    return random_string

def get_live_date_time():
    current_time = datetime.now()
    live_date_time = current_time.strftime("%Y-%m-%dT%H:%M:%S")

    one_hour_from_now = current_time + timedelta(hours=1)
    live_date_time_one_hour_later = one_hour_from_now.strftime("%Y-%m-%dT%H:%M:%S")

    return live_date_time, live_date_time_one_hour_later

def generateMeetUrl():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(get_file_path("token.json")):
        creds = Credentials.from_authorized_user_file(get_file_path("token.json"), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(get_file_path("credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(get_file_path("token.json"), "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        # print("Getting the upcoming 10 events")
        # events_result = (
        #     service.events()
        #     .list(
        #         calendarId="primary",
        #         timeMin=now,
        #         maxResults=10,
        #         singleEvents=True,
        #         orderBy="startTime",
        #     )
        #     .execute()
        # )
        # events = events_result.get("items", [])

        # if not events:
        #     print("No upcoming events found.")

        # Prints the start and name of the next 10 events
        # for event in events:
        #     start = event["start"].get("dateTime", event["start"].get("date"))
        #     print(start, event["summary"])

    except HttpError as error:
        print("An error occurred: %s" % error)
    
        # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    event = {
        'summary': 'Google Meet Session',
        'description': 'Join the meeting',
        'start': {
            'dateTime': f'{get_live_date_time()[0]}',  # Set your desired start time here
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': f'{get_live_date_time()[1]}',
            'timeZone': 'Asia/Kolkata'
        },
        'conferenceData': {
            'createRequest': {
                'requestId': f'{generate_random_string()}',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        }
    }

    event = service.events().insert(calendarId="primary", body=event, conferenceDataVersion=1).execute()
    
    event_url = event.get('hangoutLink')
    # print(f'Event created: {event_url}')
    return event_url
    
if __name__ == "__main__":
    generateMeetUrl()

# [END calendar_quickstart]