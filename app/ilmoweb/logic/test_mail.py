from django.core.mail import send_mail
from django.conf import settings
import time

def mail():

    time.sleep(6.5)

    subject = 'Test Email from ilmoweb'
    message = 'This is a test email sent from ilmoweb.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['testi1@meloni.dev',
                      'testi2@meloni.dev',
                      'testi3@meloni.dev',
                      'testi4@meloni.dev',
                      'testi5@meloni.dev',
                      'testi6@meloni.dev',
                      'testi7@meloni.dev',
                      'testi8@meloni.dev',
                      'testi9@meloni.dev',
                      'testi10@meloni.dev',
                      'testi11@meloni.dev',
                      'testi12@meloni.dev']

    send_mail(subject, message, from_email, recipient_list)