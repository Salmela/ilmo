"""Module for app logic."""
from ilmoweb.models import Report
import datetime

def save_report(user, lab_group, filename):
    """
        save report to database
    """
    if filename:
        report_status = 1
    else:
        report_status = 0

    send_date = datetime.date.today

    report = Report(user=user, lab_group=lab_group, send_date=send_date, filename=filename, report_status=report_status)
    report.save()
