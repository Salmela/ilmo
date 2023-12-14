"""Module for populating relations."""
import sys
from django.contrib.auth.hashers import make_password

sys.path.append('./')

"""
    Django needs the wsgi import to configure settings and download apps.

"""
import wsgi

from ilmoweb.models import Courses

course = Courses(name="Vanhanmalliset työt", description="Vanhanmalliset Fysikaalisen kemian perustyöt A (A3, A4, A5) sekä (TD3, TD5, TD7, TD8, TD9) + vanha loppukuulustelu", labs_amount=8, is_visible=0)
course.save()