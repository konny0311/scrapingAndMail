import sys
sys.path.append('../')
from mainProcess import *
import datetime
import os
from apiclient.discovery import build
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64
from httplib2 import Http
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets
import googleapiclient
from apscheduler.schedulers.blocking import BlockingScheduler

def regularProcessJapan():
    #This code is executed to get stock info everyday.
    #exec this code every 15:30pm Japan time
    dayOfWeek = datetime.datetime.today().weekday()
    if 0 <= dayOfWeek and dayOfWeek <= 4: #work on weekdays
        manager = MongoDBManager.MongoDBManager()
        stockDB = manager.getDB("stock")
        japanCompanyList = getCompanyList(manager, 'japan')
        if japanCompanyList is not None:
            getFromNikkeiScraping(japanCompanyList)

def regularProcessUs():
    #This code is executed to get stock info everyday.
    #exec this code every 6:00am Japan time
    dayOfWeek = datetime.datetime.today().weekday()
    if 1 <= dayOfWeek and dayOfWeek <= 5: #work on weekdays
        manager = MongoDBManager.MongoDBManager()
        stockDB = manager.getDB("stock")
        usCompanyList = getCompanyList(manager, 'us')
        if usCompanyList is not None:
            getFromYFUSScraping(usCompanyList)

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
    store = file.Storage(os.environ['GMAILTOKEN'])
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.environ['GMAILCREDENTIALS'], SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

def autoSending():
    dayOfWeek = datetime.datetime.today().weekday()
    if 0 <= dayOfWeek and dayOfWeek <= 5: #work on weekdays + on Satruday
        sender = os.environ['MYGMAILACCOUNT']
        to = os.environ['MYGMAILACCOUNT']
        subject = generateText()
        message_text = 'test test'
        message = create_message(sender, to, subject, message_text)
        service = getService()
        user_id = os.environ['MYGMAILACCOUNT']
        send_message(service,user_id,message)

sc = BlockingScheduler(timezone='UTC')
sc.add_job(autoSending, 'cron', hour=21, minute=00) #6:00am in Japan
sc.add_job(regularProcessJapan, 'cron', hour=06, minute=30) #15:30am in Japan
sc.add_job(regularProcessUs, 'cron', hour=20, minute=00) #16:00pm in NY
sc.start()
