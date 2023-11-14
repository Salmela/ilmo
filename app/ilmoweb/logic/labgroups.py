"""Module for app logic."""
from ilmoweb.models import LabGroups

def confirm(group_id):
    """
        sets labgroup's status to "confirmed"
    """
    group = LabGroups.objects.get(pk=group_id)
    group.status = 2
    group.save()

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
    