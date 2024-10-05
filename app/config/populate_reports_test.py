"""Module for populating relations."""
import sys

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import Report, User, LabGroups
from datetime import date, time

"""
    Populates the relation conncted to the Reports with test data.

"""
with open('config/test_data_8.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(';')
        send_date = [int(i) for i in parts[2].split(',')]
        grading_date = [int(i) for i in parts[6].split(',')]
        report = Report(
            student=User.objects.get(pk=parts[0]),
            lab_group=LabGroups.objects.get(pk=parts[1]),
            send_date=date(send_date[0], send_date[1], send_date[2]),
            report_status=parts[3],
            comments=parts[4],
            grade=parts[5],
            grading_date=date(grading_date[0], grading_date[1], grading_date[2]),
            graded_by=User.objects.get(pk=parts[7])
        )
        report.save()