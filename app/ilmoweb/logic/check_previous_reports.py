"""Module for app logic."""
from django.contrib import messages
from ilmoweb.models import Report

def check_and_replace(request, prev_1, prev_2, prev_3, prev_4, student, lab_group, file):
    if prev_4:
        messages.warning(request, "Et voi palauttaa tähän työhön uutta raporttia")

    if prev_3:
        Report.objects.filter(pk=prev_3[0].id).delete()
        report = Report(student=student, lab_group=lab_group, filename=file, report_status=3)
        report.save()
        messages.success(request, "Korjausehdotukset sisältävä tiedosto korvattu uudella")

    if prev_2:
        report = Report(student=student, lab_group=lab_group, filename=file, report_status=3)
        report.save()
        messages.success(request, "Korjausehdotukset sisältävä tiedosto lähetetty onnistuneesti")

    if prev_1:
        Report.objects.filter(pk=prev_1[0].id).delete()
        report = Report(student=student, lab_group=lab_group, filename=file, report_status=1)
        report.save()
        messages.success(request, "Alkuperäisen korvaava tiedosto lähetetty onnistuneesti")

    else:
        report = Report(student=student, lab_group=lab_group, filename=file, report_status=1)
        report.save()
        messages.success(request, "Tiedosto lähetetty onnistuneesti")

    return