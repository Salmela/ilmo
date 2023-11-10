"""Module for routing urls."""
import environ
from django.urls import path, include

from . import views

env = environ.Env()
environ.Env.read_env()

if env('LOCAL') == 'True':
    urlpatterns = [
        path("", views.home_page_view, name="home"),
        path("accounts/", include("django.contrib.auth.urls")),
        path("created_labs/", views.created_labs, name="created_labs"),
        path("create_lab/", views.create_lab, name="create_lab"),
        path("open_labs/", views.open_labs, name="open_labs"),
        path("open_labs/enroll/", views.enroll, name="enroll"),
        path("open_labs/confirm/", views.confirm, name="confirm"),
        path("cancel_enrollment/<int:labgroup_id>", views.cancel_enrollment, name="cancel_enrollment"),
        path("make_lab_visible/<int:lab_id>", views.make_lab_visible, name="make_lab_visible"),
        path("delete_lab/<int:lab_id>", views.delete_lab, name="delete_lab"),
        path("my_labs/", views.my_labs, name="my_labs"),
        path("create_group/", views.create_group, name="create_group"),
        path("return_report/", views.return_report, name="return_report"),
        path("returned_reports/", views.returned_reports, name="returned_reports"),
        path("returned_report/<int:report_id>", views.returned_report, name="returned_report"),
        path("evaluate_report/<int:report_id>", views.evaluate_report, name="evaluate_report"),
        path("download_report/<str:filename>", views.download_report, name="download_report"),
        path("delete_labgroup/<int:labgroup_id>", views.delete_labgroup, name="delete_labgroup"),
        path("labgroup_status/<int:labgroup_id>", views.labgroup_status, name="labgroup_status")
    ]

if env('LOCAL') == 'False':
    urlpatterns = [
        path("", views.home_page_view, name="home"),
        path("accounts/", include("django.contrib.auth.urls")),
        path("created_labs/", views.created_labs, name="created_labs"),
        path("create_lab/", views.create_lab, name="create_lab"),
        path("open_labs/", views.open_labs, name="open_labs"),
        path("open_labs/enroll/", views.enroll, name="enroll"),
        path("open_labs/confirm/", views.confirm, name="confirm"),
        path("cancel_enrollment/<int:labgroup_id>", views.cancel_enrollment, name="cancel_enrollment"),
        path("make_lab_visible/<int:lab_id>", views.make_lab_visible, name="make_lab_visible"),
        path("delete_lab/<int:lab_id>", views.delete_lab, name="delete_lab"),
        path("my_labs/", views.my_labs, name="my_labs"),
        path("create_group/", views.create_group, name="create_group"),
        path("return_report/", views.return_report, name="return_report"),
        path("returned_reports/", views.returned_reports, name="returned_reports"),
        path("returned_report/<int:report_id>", views.returned_report, name="returned_report"),
        path("evaluate_report/<int:report_id>", views.evaluate_report, name="evaluate_report"),
        path("download_report/<str:filename>", views.download_report, name="download_report"),
        path("delete_labgroup/<int:labgroup_id>", views.delete_labgroup, name="delete_labgroup"),
        path("labgroup_status/<int:labgroup_id>", views.labgroup_status, name="labgroup_status"),
        path('login/', views.login, name='login'),
        path('auth/', views.auth, name='auth'),
        path('logout/', views.logout, name='logout')
    ]