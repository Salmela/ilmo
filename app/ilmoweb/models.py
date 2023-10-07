"""Module for models."""
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
        Model for user-data

    """
    student_id = models.IntegerField(default=000000000)

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
    max_students = models.IntegerField()
    minim_students = models.IntegerField(default=2)
    is_visible = models.BooleanField()

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
    ## 0 = not visible to students, 1 = unconfirmed, 2 = confirmed, 3 = canceled
    signed_up_students = models.IntegerField(default=0)

class SignUp(models.Model):
    """
        Model for users and the labgroups they have signed up for
        
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    labgroups = models.ForeignKey(LabGroups, on_delete=models.CASCADE)
    