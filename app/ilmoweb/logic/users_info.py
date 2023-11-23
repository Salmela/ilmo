"""Module for app logic."""
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages


def change_email(request, user, new_email):
    """ 
        Changes user's email address after checking that it's valid
    """
    try:
        validate_email(new_email)
    except ValidationError:
        messages.warning(request, "Syötä oikeassa muodossa oleva sähköpostiosoite")
    else:
        user.email = new_email
        user.save()
        messages.success(request, "Sähköpostiosoite päivitetty")
