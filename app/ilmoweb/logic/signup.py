"""Module for app logic."""
from ilmoweb.models import  SignUp# pylint: disable=unused-import


def signup(user, group):
    """
        Creates a new SignUp database object if user hasn't already signed up

    """
    if SignUp.objects.filter(user=user, labgroups = group):
        raise Exception
    signup = SignUp(user=user, labgroups=group)
    signup.save()