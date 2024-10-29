"""Module for populating relations."""
import sys

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import User

user = User.objects.get(username="korkella")
user.is_staff=1
user.is_superuser=1
user.save()