import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


def send_email():
    from_email = Email('praveengowtham.pg@gmail.com')
    to_email = To('mohamedriyazafzal@gmail.com')
    subject = 'Sending with SendGrid is Fun'
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)

    try:
        sg = SendGridAPIClient('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')
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


send_email()