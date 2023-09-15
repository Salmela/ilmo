"""Module for populating relations."""
import sys

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import User


"""
    Populates the relation connected to the User model with test data.

"""
with open('config/data.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(';')
        user = User(student_id=parts[0], username=parts[1], password=parts[2], name=parts[3], surname=parts[4], email=parts[5])
        user.save()