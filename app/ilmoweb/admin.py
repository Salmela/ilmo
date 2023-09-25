"""Module for Django admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Courses, Labs, LabGroups

admin.site.register(User, UserAdmin)
admin.site.register(Courses)
admin.site.register(Labs)
admin.site.register(LabGroups)
