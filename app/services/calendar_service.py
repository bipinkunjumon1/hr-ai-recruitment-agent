import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


class CalendarService:

    def __init__(self):

        self.service = self.authenticate()

    def authenticate(self):

        creds = None

        if os.path.exists("token.json"):

            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        if not creds:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

            with open(
                "token.json",
                "w"
            ) as token:

                token.write(
                    creds.to_json()
                )

        return build(
            "calendar",
            "v3",
            credentials=creds
        )

    def schedule_interview(
        self,
        candidate_name,
        candidate_email,
        start_time,
        end_time
    ):

        event = {

            "summary":
            f"Interview - {candidate_name}",

            "description":
            "HR AI Recruitment Agent Interview",

            "start": {
                "dateTime": start_time,
                "timeZone": "Asia/Kolkata"
            },

            "end": {
                "dateTime": end_time,
                "timeZone": "Asia/Kolkata"
            },

            "attendees": [
                {
                    "email": candidate_email
                }
            ],

            "conferenceData": {
                "createRequest": {
                    "requestId":
                    f"interview-{candidate_name}"
                }
            }
        }

        return (
            self.service.events()
            .insert(
                calendarId="primary",
                body=event,
                conferenceDataVersion=1,
                sendUpdates="all"
            )
            .execute()
        )