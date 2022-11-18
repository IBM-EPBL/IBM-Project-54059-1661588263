import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


def send_email():
    from_email = Email('chandhru588@gmail.com')
    to_email = To('athivignesh123@gmail.com')
    subject = 'Sending with SendGrid is Fun'
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)

    try:
        sg = SendGridAPIClient('tMbrLvEdQDaABgeT1SIL1A')
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


send_email()