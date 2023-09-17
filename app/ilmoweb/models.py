"""Module for models."""
from django.db import models

class User(models.Model):
    """
        Model for user-data

    """
    student_id = models.IntegerField()
    username = models.TextField()
    password = models.TextField()
    name = models.TextField()
    surname = models.TextField()
    email = models.TextField()

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
    is_visible = models.BooleanField()
