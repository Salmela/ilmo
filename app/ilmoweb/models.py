"""Module for models."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_cryptography.fields import encrypt

class User(AbstractUser):
    """
        Model for user-data

    """
    student_id = encrypt(models.CharField(default="000000000"))
    first_name = encrypt(models.CharField(max_length = 100))
    last_name = encrypt(models.CharField(max_length = 100))
    email = encrypt(models.CharField(max_length = 100))

class Courses(models.Model):
    """
        Model for courses

    """
    name = models.CharField(max_length = 100)
    description = models.TextField()
    labs_amount = models.IntegerField()
    is_visible = models.BooleanField()

class Labs(models.Model):
    """
        Model for labs

    """
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    max_students = models.IntegerField(default= 1)
    is_visible = models.BooleanField()
    deleted = models.BooleanField(default=0)

class LabGroups(models.Model):
    """
        Model for groups

    """
    lab = models.ForeignKey(Labs, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    place = models.CharField(max_length = 100)
    status = models.IntegerField(default = 0)
    # 0 = not visible to students, 1 = unconfirmed, 2 = confirmed, 3 = canceled
    signed_up_students = models.IntegerField(default=0)
    assistant = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField(default=0)

class SignUp(models.Model):
    """
        Model for users and the labgroups they have signed up for

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    labgroups = models.ForeignKey(LabGroups, on_delete=models.CASCADE)

class Report(models.Model):
    """
        Model for reports

    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "student")
    lab_group = models.ForeignKey(LabGroups, on_delete=models.CASCADE)
    send_date = models.DateField(auto_now_add=True)
    report_file = models.FileField(upload_to="ilmoweb/static/upload/", null=True)
    report_file_name = models.CharField(default="")
    report_status = models.IntegerField()
    # 0 = no file, 1 = report returned, 2 = revisions proposed, 3 = fixed report, 4 = report graded
    comments = models.TextField()
    comment_file = models.FileField(upload_to="ilmoweb/static/upload/", null=True)
    comment_file_name = models.CharField(default="")
    grade = models.IntegerField(null=True)
    # 0 = revisions needed, 1-5 = grade, empty = not graded
    grading_date = models.DateField(null=True)
    graded_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name = "grader"
    )

class TeachersMessage(models.Model):
    message = models.TextField()
