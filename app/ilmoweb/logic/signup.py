"""Module for app logic."""
from ilmoweb.models import SignUp, Labs


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
