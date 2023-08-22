import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
            if username is None:
                required_fields = user_model.REQUIRED_FIELDS
                for required_field in required_fields:
                    username = kwargs.get(required_field)
                    if username is not None:
                        break
        if username is None or password is None:
            return
        try:
            phone_regex = r"^\+[0-9]{9,15}$"
            if re.match(phone_regex, username):
                user = user_model._default_manager.get(**{'phone': username})
            else:
                # CaseInsensitiveModelBackend
                case_insensitive_username_field = '{}__iexact'.format(user_model.USERNAME_FIELD)
                user = user_model._default_manager.get(**{case_insensitive_username_field: username})
        except user_model.DoesNotExist:
            user_model().set_password(password)
        else:
            if user.check_password(password):
                if self.user_can_authenticate(user):
                    return user
                else:
                    return None

    # django.contrib.auth.backends.AllowAllUsersModelBackend
    def user_can_authenticate(self, user):
        return True
