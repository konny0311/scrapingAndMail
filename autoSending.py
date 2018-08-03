import os
import subprocess
from bs4 import BeautifulSoup #download needed
import urllib3 #download needed

def create_message(sender, to , subject, message_text):

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print ("Message Id: %s" % message["id"])
        return message
    except erros.HttpError as error:
        print("Error occurred: %s" % error)

def copyDraft():
    with open("draft.txt", "r") as file:
        data = file.read()
    pyperclip.copy(data)

#
def showHTML(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    html = response.data.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(soup)

showHTML("https://qiita.com/itkr/items/513318a9b5b92bd56185")
