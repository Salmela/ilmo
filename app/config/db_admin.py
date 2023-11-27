import sys

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import User

username = input("käyttäjänimi superuseriksi: ")

user = User.objects.get(username=username)
user.is_staff=True
user.is_superuser=True
user.save()
