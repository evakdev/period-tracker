from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

MyUser=get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email = None, password = None, **kwargs):
        try:
            user = MyUser.objects.get(email=email)