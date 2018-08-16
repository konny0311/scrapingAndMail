import os
from apiclient.discovery import build
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64
from httplib2 import Http
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
import googleapiclient
from mainProcess import generateText

SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.readonly']
def build_service(credentials):
    http = Http()
    http = credentials.authorize(http)
    return build('gmail', 'v1', http=http)

def create_message(sender, to , subject, message_text):

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    print(message.as_string())
    print(type(print(message.as_string())))
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print ('Message Id: %s' % message['id'])
        return message
    except googleapiclient.errors.HttpError as error:
        print('Error occurred: {}'.format(error))

def getService():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

sender = os.environ['MYGMAILACCOUNT']
to = os.environ['MYGMAILACCOUNT']
subject = 'Yesterdays your stocks'
message_text = generateText()
message = create_message(sender, to, subject, message_text)
service = getService()
user_id = os.environ['MYGMAILACCOUNT']
send_message(service,user_id,message)
