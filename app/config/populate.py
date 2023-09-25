"""Module for populating relations."""
import sys
from django.contrib.auth.hashers import make_password

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import User, Courses


"""
    Populates the relation connected to the User model with test data.

"""
with open('config/test_data_1.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(';')
        user = User(student_id=parts[0], username=parts[1], password=make_password(parts[2]), first_name=parts[3], last_name=parts[4], email=parts[5])
        user.save()

"""
    Populates the relation connected to the Courses model with test data.

"""
with open('config/test_data_2.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(';')
        course = Courses(name=parts[0], description=parts[1], labs_amount=parts[2], is_visible=parts[3])
        course.save()