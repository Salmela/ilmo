"""Module for custom authentication backend."""
from ilmoweb.models import User
from django.contrib.auth.hashers import make_password


class AuthenticationBackend:
    def authenticate(self, request, userinfo=None):
        try:
            user = User.objects.get(email=userinfo['email'])
        except User.DoesNotExist:
            user = User(username=userinfo['uid'], first_name=userinfo['given_name'], last_name=userinfo['family_name'], email=userinfo['email'], password=make_password("test"), is_staff=0)
            user.save()
            return user
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None