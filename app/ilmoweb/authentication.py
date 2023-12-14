"""Module for custom authentication backend."""
from django.contrib.auth.hashers import make_password
from ilmoweb.models import User


class AuthenticationBackend:
    """
        Class for custom authentication
    """
    def authenticate(self, request, userinfo=None, userdata=None):
        """
            Function for custom authentication
        """
        try:
            user = User.objects.get(username=userinfo['uid'])
        except User.DoesNotExist:

            if userdata['hyPersonStudentId'] is None:
                student_id = "000000000"
            else:
                student_id = userdata['hyPersonStudentId']

            user = User(student_id=student_id, username=userinfo['uid'],
                        first_name=userinfo['given_name'],
                        last_name=userinfo['family_name'], email=userinfo['email'],
                        password=make_password("pass"), is_staff=0)
            user.save()
            return user

        if user.student_id == "0":
            if userdata['hyPersonStudentId'] is None:
                user.student_id = "000000000"
            else:
                user.student_id=userdata['hyPersonStudentId']

        if user.email == "-":
            user.email=userinfo['email']

        return user

    def get_user(self, user_id):
        """
            Helper function for custom authentication
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
