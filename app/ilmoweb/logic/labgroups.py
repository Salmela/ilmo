"""Module for app logic."""
from ilmoweb.models import LabGroups

def confirm(group_id):
    """
        sets labgroup's status to "confirmed"
    """
    group = LabGroups.objects.get(pk=group_id)
    group.status = 2
    group.save()

def create(lab, date, start_time, end_time, place, assistant): # pylint: disable=too-many-arguments
    """
        creates new labgroup in database
    """

    group = LabGroups(lab=lab,
                      date=date,
                      start_time=start_time,
                      end_time=end_time,
                      place=place,
                      assistant=assistant)
    group.save()

def update(date, start_time, end_time, place, assistant, labgroup_id): # pylint: disable=too-many-arguments
    """
        updates labgroup in database
    """

    group = LabGroups.objects.get(pk=labgroup_id)

    group.id = labgroup_id
    group.date = date
    group.start_time = start_time
    group.end_time = end_time
    group.place = place
    group.assistant = assistant

    group.save()
    