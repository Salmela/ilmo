"""Module for app logic."""
from django.core.mail import send_mail
from ilmoweb.models import Labs, LabGroups, SignUp

def email(lab_group, message_type):
    """
        sends email to given addresses
        ----------------------------
        CURRENTLY WORKS ONLY LOCALLY
        ----------------------------
        open another terminal and go to ilmoweb/app
        run poetry shell
        run python3 -m smtpd -n -c DebuggingServer localhost:1025
    """
    lab = Labs.objects.get(pk=lab_group.lab_id)
    all_students = SignUp.objects.all()
    email_recipient_list = []
    for student in all_students:
        if student.labgroups_id == int(lab_group.id):
            email_recipient_list.append(student.user.email)
    if message_type == 'confirm':
        subject = 'Ilmoittautuminen laboratoriotyöhön hyväksytty'
        message = (
            f'Ilmoittautumisesi laboratoriotyöhön {lab.name} on hyväksytty.\n'
            f'Ajankohta: {lab_group.date.day}.{lab_group.date.month}.{lab_group.date.year} '
            f'klo {lab_group.start_time.hour} - {lab_group.end_time.hour}\n'
            f'Paikka: {lab_group.place}\n'
        )
    elif message_type == 'cancel':
        subject = 'Laboratoriotyö peruttu'
        message = (
            f'Laboratoriotyö '
            f'{lab.name} ({lab_group.date.day}.{lab_group.date.month}.{lab_group.date.year}) '
            'on peruttu.'
        )
    send_mail(
    subject,
    message,
    'ilmoweb@gmail.com',
    email_recipient_list,
    fail_silently=True
    )

def confirm(group_id):
    """
        sets labgroup's status to "confirmed"
    """
    group = LabGroups.objects.get(pk=group_id)
    group.status = 2
    group.save()
    email(group, 'confirm')

def create(lab, date, time, place, assistant):
    """
        creates new labgroup in database
    """
    if time == '8-12':
        start_time = '08'
        end_time = '12'
    if time == '12-16':
        start_time = '12'
        end_time = '16'

    group = LabGroups(lab=lab,
                      date=date,
                      start_time=start_time,
                      end_time=end_time,
                      place=place,
                      assistant=assistant)
    group.save()

def update(date, time, place, assistant, labgroup_id):
    """
        updates labgroup in database
    """
    if time == '8-12':
        start_time = '08'
        end_time = '12'
    if time == '12-16':
        start_time = '12'
        end_time = '16'

    group = LabGroups.objects.get(pk=labgroup_id)

    group.id = labgroup_id
    group.date = date
    group.start_time = start_time
    group.end_time = end_time
    group.place = place
    group.assistant = assistant

    group.save()
    