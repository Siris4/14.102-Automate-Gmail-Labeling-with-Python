import os
import pickle
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Update the path to the credentials.json file
CREDENTIALS_PATH = r'C:\Users\guber\Desktop\My_Coding_Projects\Project 14 - Get Gmail to Labeled Inbox Auto-Sorter\14.1 Get Gmail Auto-Labled and Auto-Sorted for Email v01r00\NYW_CP14.102\dont post\client_secret_834982543066-ejpvr7pd68201tve7aobh55e213qv76h.apps.googleusercontent.com.json'

def authenticate_gmail():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)  # Ensure the path to 'credentials.json' is correct
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_service():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_emails(service, query=''):
    # Call the Gmail API
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_message(service, msg_id):
    message = service.users().messages().get(userId='me', id=msg_id).execute()
    return message

def modify_message(service, msg_id, add_labels=[], remove_labels=[]):
    msg_labels = {
        'addLabelIds': add_labels,
        'removeLabelIds': remove_labels
    }
    message = service.users().messages().modify(userId='me', id=msg_id, body=msg_labels).execute()
    return message

def auto_label_emails(service):
    emails = list_emails(service, query='is:unread')
    for email in emails:
        msg = get_message(service, email['id'])
        # Define your criteria here. Example: if subject contains "Important"
        if 'Important' in msg['snippet']:
            modify_message(service, email['id'], add_labels=['Label_1'], remove_labels=[])

if __name__ == '__main__':
    service = get_service()
    auto_label_emails(service)
