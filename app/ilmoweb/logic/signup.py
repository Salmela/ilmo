"""Module for app logic."""
from ilmoweb.models import SignUp


def signup(user, group):
    """
        Creates a new SignUp database object if user hasn't already signed up

    """
    if SignUp.objects.filter(user=user, labgroups = group):
        raise ValueError('Already signed up')
    signup_to_group = SignUp(user=user, labgroups=group)
    signup_to_group.save()
