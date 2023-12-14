"""Module for populating relations."""
import sys

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import Courses, Labs

A_kurssi = Courses.objects.get(name="Vanhanmalliset työt")

lab = Labs(name="Loppukuulustelu", description="Töiden loppukuulustelu", max_students=50, is_visible=0, deleted=1, course=A_kurssi)
lab.save()

with open('config/labs_final.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(',')
        lab = Labs(name=parts[1], description=parts[2], max_students=parts[4], is_visible=0, deleted=1, course=A_kurssi)
        lab.save()

