"""Module for populating relations."""
import sys
from django.contrib.auth.hashers import make_password

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import User

"""
    Populates the relation connected to the User model with official data.

"""

with open('config/users.csv') as file:
    x = 1
    for line in file:
        line = line.replace('\n','')
        parts = line.split(';')

        student_id = parts[1]
        username = parts[0]
        password = make_password("pass")
        first_name = parts[2]
        last_name = parts[3]

        email = parts[4]
        if parts[4] == "":
            email = "None"

        is_staff = 0
        is_superuser = 0
        if parts[5] == "0":
            is_staff = 0
            is_superuser = 0
        elif parts[5] == "1":
            is_staff = 1
            is_superuser = 0
        elif parts[5] == "2":
            is_staff = 1
            is_superuser = 1

        user = User(student_id=student_id, username=username, password=password, first_name=first_name,
                    last_name=last_name, email=email, is_staff=is_staff, is_superuser=is_superuser)
        user.save()

        print(x)
        x+=1