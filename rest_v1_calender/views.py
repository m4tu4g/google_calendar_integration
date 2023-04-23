import datetime
import os

from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect

import google_apis_oauth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# OAuth doesn't allow http unsecured connections for
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
CLIENT_ID_FILE = "credentials.json"
BASE_URI = 'http://127.0.0.1:8000/rest/v1/calender/'
REDIRECT_URI = BASE_URI + 'redirect/'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def GoogleCalendarInitView(request):
    oauth_url = google_apis_oauth.get_authorization_url(
        CLIENT_ID_FILE, SCOPES, REDIRECT_URI)
    return HttpResponseRedirect(oauth_url)

# Code taken from https://developers.google.com/calendar/api/quickstart/python


def GoogleCalendarRedirectView(request):
    try:
        # Get user credentials
        creds = google_apis_oauth.get_crendentials_from_callback(
            request,
            CLIENT_ID_FILE,
            SCOPES,
            REDIRECT_URI
        )
        # creds_json = creds.to_json()
    except:
        return HttpResponse("Login failed / expired")

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return HttpResponse('No upcoming events found.')

        events_response = []
        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            events_response.append(start + " " + event['summary'])

    except HttpError:
        return HttpResponse('Error occurred')

    return HttpResponse(events_response)
