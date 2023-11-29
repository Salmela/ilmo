import sys

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import User

value = input("Lisää superuser1, Poista käyttäjä 2: ")

if value == "1":
    username = input("käyttäjänimi superuseriksi: ")

    user = User.objects.get(username=username)
    user.is_staff=True
    user.is_superuser=True
    user.save()

if value == "2":
    username = input("poista käyttäjänimi: ")
    user = User.objects.get(username=username)
    user.delete()
