from django.core.mail import send_mail,EmailMessage

import os

class Util:
    @staticmethod
    def send_mail(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            to=[data['to_email']]
        )
        email.send()