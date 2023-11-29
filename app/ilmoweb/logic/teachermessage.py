"""Module for app logig"""
from ilmoweb.models import TeachersMessage

def update(new_message):
    messages = TeachersMessage.objects.all()

    if len(messages) == 0:
        message=TeachersMessage(message=new_message)
        message.save()
    else:
        messages[0].message = new_message
        messages[0].save()