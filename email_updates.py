import base64
import os.path
from datetime import datetime
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

now = datetime.now() # Current date/time
message_header = 'FOR CPE IRB' + '\n' + '*'*60 + '\n'
message_footer = '\n' + 'Sent from CPE Python Script' + '\n' + '*'*60
#Check if alerts are active:
path = os.getcwd() + '/**/*'

if os.path.isfile('sci_alerts.txt'):
    print('Science Alerts Detected')
    sci_alerts = open('sci_alerts.txt', 'r')
else:
    sci_alerts = 'No Science Team Alerts'

if os.path.isfile('former.txt'):
    print('Employee Changes Detected')
    former_alerts = open('former.txt', 'r')
else:
    former_alerts = "No Other Updates"

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)
message = MIMEText(message_header + sci_alerts.read() + '\n' + former_alerts.read() + message_footer)
message['to'] = 'CPEIRB@policingequity.org'
message['subject'] = 'CITI UPDATE:' + ' ' + now.strftime("%m - %d - %Y")
create_message = {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}

try:
    message = (service.users().messages().send(userId="me", body=create_message).execute())
    print('Successfully sent message.')
except HTTPError as error:
    print(F'An error occurred: {error}')
    message = None