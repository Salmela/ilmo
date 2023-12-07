"""Module for populating relations."""
import sys
from django.contrib.auth.hashers import make_password

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import User, Courses, Labs, LabGroups
from datetime import date, time


"""
    Populates the relation connected to the User model with official data.

"""
with open('config/test_data_1.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(';')
        user = User(student_id=parts[0], username=parts[1], password=make_password(parts[2]), first_name=parts[3], last_name=parts[4], email=parts[5], is_staff=parts[6])
        user.save()

"""
    Sets superuser.

"""
user = User.objects.get(pk=1)
user.is_superuser=1
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

"""
    Populates the relation connected to the Labs with test data.

"""
with open('config/test_data_3.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(';')
        lab = Labs(name=parts[0], description=parts[1], max_students=parts[2], is_visible=parts[3],course_id=parts[4])
        lab.save()

"""
    Populates the relation conncted to the LabGroups with test data.

"""
with open('config/test_data_4.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(';')
        test_date = [int(i) for i in parts[0].split(',')]
        group = LabGroups(
            date=date(test_date[0], test_date[1], test_date[2]),
            start_time=time(int(parts[1])),
            end_time=time(int(parts[2])),
            place=parts[3],
            status=parts[4],
            lab_id=parts[5]
        )
        group.save()