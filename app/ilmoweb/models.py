"""Module for models."""
from django.db import models    # pylint: disable=unused-import

class User(models.Model):
    student_id = models.IntegerField()
    username = models.TextField()
    password = models.TextField()
    name = models.TextField()
    surname = models.TextField()
    email = models.TextField()