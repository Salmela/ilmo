"""Module for app logic."""
from ilmoweb.models import SignUp, Labs, LabGroups


def signup(user, group):
    """
        Creates a new SignUp database object if user hasn't already signed up

    """
    if SignUp.objects.filter(user=user, labgroups = group):
        raise ValueError('Already signed up')

    lab = Labs.objects.get(pk=group.lab_id)
    if group.signed_up_students < lab.max_students:
        signup_to_group = SignUp(user=user, labgroups=group)
        signup_to_group.save()

        group.signed_up_students += 1
        group.save()
    else:
        raise ValueError('The group has no open spots left')

def get_labgroups(usr):
    """
        Fetches all labgroups based on user_id
    """
    labgroups = SignUp.objects.filter(user=usr).values()
    labgroups_id = []
    if labgroups:
        for obj in labgroups:
            labgroups_id.append(obj["labgroups_id"])
    return labgroups_id

def cancel(user, group_id):
    """
        Cancels user's enrollment for the group
    """
    enrollment = SignUp.objects.get(labgroups_id = group_id, user_id = user.id)

    if not enrollment:
        raise ValueError('Enrollment for the group was not found')
    enrollment.delete()

    group = LabGroups.objects.get(pk=group_id)
    group.signed_up_students -= 1
    group.save()
