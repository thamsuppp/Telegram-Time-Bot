#OAuth2.0 Setup
from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import datetime, timedelta
import datefinder

#Specify scopes - this one allows access to Calendars (least restrictive)
scopes = ['https://www.googleapis.com/auth/calendar']
#Create flow, using client_secrets json file and the scopes
#flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes = scopes)

#Load pickle file of credentials
credentials = pickle.load(open('token.pkl', 'rb'))

#Create service object for the Calendar API
service = build('calendar', 'v3', credentials = credentials)


##Get calendars
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']


#Parse events

def get_calendar_events(n_days_ahead = 1):

    #Get timeMin: time now
    time_now = datetime.now()

    #Get timeMax: time n_days_ahead from now
    time_max = time_now + timedelta(days = n_days_ahead)

    #Getting the events for a certain calendar
    events = service.events().list(calendarId = calendar_id, 
        timeMin = datetime.strftime(time_now, '%Y-%m-%dT%H:%M:%S') + '-04:00', 
        timeMax = datetime.strftime(time_max, '%Y-%m-%dT%H:%M:%S') + '-04:00').execute()

    out_string = ''

    for event in events['items']:
        date_string = event['start']['dateTime']
        date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
        out_string = out_string + '{}, {} \n'.format(event['summary'], date.strftime('%m/%d %H:%M'))

    return out_string

#Create event
def create_event(summary, start_time_str, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

    #Return string output confirming that event was added
    out = '''
    Event created successfully.
    Summary: {}
    Start: {}
    End: {}
    '''.format(created_event['summary'], created_event['start']['dateTime'], created_event['end']['dateTime'])

    return out




