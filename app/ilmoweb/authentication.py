"""Module for custom authentication backend."""
from django.contrib.auth.hashers import make_password
from ilmoweb.models import User


class AuthenticationBackend:
    """
        Class for custom authentication
    """
    def authenticate(self, request, userinfo=None):
        """
            Function for custom authentication
        """
        try:
            user = User.objects.get(username=userinfo['uid'])
        except User.DoesNotExist:
            user = User(username=userinfo['uid'], first_name=userinfo['given_name'],
                        last_name=userinfo['family_name'], email=userinfo['email'],
                        password=make_password("test"), is_staff=0)
            user.save()
            return user
        return user

    def get_user(self, user_id):
        """
            Helper function for custom authentication
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
