#CITI Email Updater
#Jonathan A. LLoyd, Research Associate
#Center for Policing Equity
#Last Updated: May 20 2024

print('~'* 60)
print('CITI Email Updater')
print('Center for Policing Equity OHRP')
print('v.1.5')
print('2024', '\n')
print('~'*60)

import base64
import os.path
from datetime import datetime
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

now = datetime.now() # Current date/time
message_header = 'FOR CPE IRB' + '\n' + '*'*60 + '\n'
message_footer = '*'*60 + '\n' + 'Sent from CPE Python Script' + '\n' + '*'*60
#Check if alerts are active:
path = os.getcwd() + '/**/*'

if os.path.isfile('sci_alerts.txt'):
    print('Science Alerts Detected')
else:
    with open('sci_alerts.txt', 'w') as file:
        file.write('No Science Team Alerts')
        file.close()
sci_alerts = open('sci_alerts.txt', 'r')

if os.path.isfile('former.txt'):
    print('Employee Changes Detected')
else:
    with open('former.txt', 'w') as file:
        file.write("No Other Employee Updates")
        file.close()
former_alerts = open('former.txt', 'r')

if os.path.isfile('alerts.txt'):
    print('Key Personnel Alerts Detected')
else:
    with open('alerts.txt', 'w') as file:
        file.write('No Key Personnel Alerts')
        file.close()
key_alerts = open('alerts.txt', 'r')

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)
message = MIMEText(message_header + sci_alerts.read() + '\n' + key_alerts.read() + '\n' + former_alerts.read() + '\n' + message_footer)
message['to'] = 'CPEIRB@policingequity.org'
message['subject'] = 'CITI UPDATE:' + ' ' + now.strftime("%m - %d - %Y")
create_message = {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}

try:
    message = (service.users().messages().send(userId="me", body=create_message).execute())
    print('Successfully sent message.')
except HTTPError as error:
    print(F'An error occurred: {error}')
    message = None
