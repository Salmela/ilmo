"""Module for app logic."""
from django.db.models import Max, F, Subquery, OuterRef
from ilmoweb.models import Report

def filter_report(user_id):
    """
        Function to filter the report with highest status per labgroup
    """
    reports = Report.objects.filter(student=user_id)
    subquery = reports.filter(lab_group=OuterRef("lab_group")).values("lab_group").annotate(
    max_report_status=Max("report_status")).values("max_report_status")
    reports = reports.annotate(max_report_status=Subquery(subquery))
    filtered_reports = reports.filter(report_status=F("max_report_status"))
    return filtered_reports
