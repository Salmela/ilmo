from django.core.mail import send_mail
from django.conf import settings
import time

def mail():

    time.sleep(7)

    subject = 'Test Email from ilmoweb'
    message = 'This is a test email sent from ilmoweb.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['ella.korkeaaho@gmail.com']

    send_mail(subject, message, from_email, recipient_list)