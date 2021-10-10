
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, date_of_birth, password=None):
        if not email:
            raise ValueError("Email should be set")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password=password)
        user.username = username
        user.date_of_birth = date_of_birth
        user.save()
        return user

    def create_superuser(self, email, username, date_of_birth, password=None):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.username = username
        user.date_of_birth = date_of_birth
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    default_pfp_url = "https://i.ibb.co/k9RDpkG/default-pfp.png"
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    numeroid = models.CharField(max_length=4)
    unique_id = models.CharField(max_length=55)
    date_of_birth = models.DateField()
    picture = models.URLField(default=default_pfp_url)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "date_of_birth"]

    objects = MyUserManager()

    def save(self, *args, **kwargs):
        while True:
            numeroid = str(random.randrange(1, 10000)).zfill(4)
            unique_id = f"{self.username}#{numeroid}"

            try:
                checking = get_user_model().objects.get(unique_id=unique_id)
            except:
                self.numeroid = numeroid
                self.unique_id = unique_id
                super().save(*args, **kwargs)
                return

    @property
    def trackables(self):
        trackables = self.categories.first().trackables.none()
        for category in self.categories.all():
            trackables = trackables.union(category.trackables.all())
        return trackables

    def category_name_is_duplicate(self, name):
        category_names = self.categories.values_list("name", flat=True)
        clean_name = name.lower().strip()
        return clean_name in category_names

    def trackable_name_is_duplicate(self, name):
        trackable_names = self.trackables.values_list("name", flat=True)
        clean_name = name.lower().strip()
        return clean_name in trackable_names

    def __str__(self):
        return self.unique_id
