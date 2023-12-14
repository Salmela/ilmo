"""Module for populating relations."""
import sys
from django.contrib.auth.hashers import make_password

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import User, Courses, Labs, LabGroups, Report
from datetime import date, time


labrat = {}
labrat[25] = "Metyylipunan happovakion määritys"
labrat[23] = "Atomin spektri"
labrat[27] = "Ab initio"
labrat[24] = "Molekyylin elektroninen värähdysspektri"
labrat[34] = "Nesteen höyrynpaineen lämpötilariippuvuus"
labrat[32] = "Pommikalorimetria"
labrat[36] = "KULJETUSLUVUN MÄÄRITTÄMINEN"
labrat[35] = "Kaasureaktion kinetiikka"
labrat[50] = "Polttokenno"
labrat[37] = "Kiniinin fluoresenssi"
labrat[33] = "Liuoskalorimetria"
labrat[38] = "Reaktiokinetiikan tietokoneharjoitus"
labrat[53] = "Molekyylin infrapunaspektri"
labrat[56] = "Metyylipunan happovakion määritys"
labrat[59] = "Molekyylin infrapunaspektri"
labrat[54] = "Atomin spektri"
labrat[55] = "Molekyylin elektroninen värähdysspektri"
labrat[57] = "Laskennallinen spektroskopia"
labrat[58] = "Loppukuulustelu"


ind = {}
x = 1

with open('config/groups_final.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(',')
        ind[parts[0]] = x
        x+=1


with open('config/groups_final.csv') as file:
    for line in file:
        line = line.replace('\n','')
        parts = line.split(',')
        assistant = None

        try:
            user = User.object.get(username=parts[3])
            assistant = user
        except:
            pass

        group = LabGroups(
            id=ind.get(parts[0]),
            date=date(2023, 1, 1),
            start_time=time(int(1)),
            end_time=time(int(1)),
            place="-",
            status=0,
            assistant=assistant,
            lab=Labs.objects.get(name=labrat.get(int(parts[2]))),
            deleted=1
        )
        group.save()



comments_list = []

with open('config/comments.txt') as file:
    for line in file:
        line = line.replace('\n','')
        comments_list.append(line)


with open('config/reports_final.csv') as file:
    x = 1
    for line in file:
        line = line.replace('\n','')
        parts = line.split(',')

        student = None
        try:
            User.objects.get(username=parts[1])
            student = User.objects.get(username=parts[1])
        except:
            student = None

        lab_group = LabGroups.objects.get(pk=int(ind.get(parts[2])))

        send_date = parts[3]
        if send_date == "NULL":
            send_date = None
        else:
            for i in range(0,len(parts[3])):
                if parts[3][i] == " ":
                    send_date=(parts[3])[:i]

        report_file_name=parts[4]
        report_status = parts[5]
        comments = comments_list.pop(0)

        grade = parts[6]
        if grade == "NULL":
            grade = 0
        else:
            grade = parts[6]

        grading_date = parts[7]
        if grading_date == "NULL":
            grading_date = None
        else:
            for i in range(0,len(parts[7])):
                if parts[7][i] == " ":
                    grading_date=(parts[7])[:i]

        graded_by = None
        try:
            User.objects.get(username=parts[8])
            graded_by = User.objects.get(username=parts[8])
        except:
            graded_by = None


        report = Report(student=student, lab_group=lab_group, send_date=send_date, report_file_name=report_file_name, report_status=report_status, comments=comments, grade=grade, grading_date=grading_date, graded_by=graded_by)
        report.save()

        print(x)
        x+=1