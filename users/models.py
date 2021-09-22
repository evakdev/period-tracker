
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE

from tracking.models import Category, Cycle, Trackable


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
    default_pfp_url = "https://media.discordapp.net/attachments/709534905733873775/863456819291488296/duck-2-128_1.png"
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    numeroid = models.CharField(max_length=4)
    unique_id = models.CharField(max_length=55)
    date_of_birth = models.DateField()
    picture = models.URLField(default=default_pfp_url)
    categories = models.ManyToManyField(Category, related_name="user_categories", null=True ,blank=True)
    trackables = models.ManyToManyField(Trackable, related_name="user_trackables", null=True ,blank=True)
    cycles = models.ForeignKey(Cycle, on_delete=CASCADE, related_name="user_cycles", null=True ,blank=True)

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

    def __str__(self):
        return self.unique_id
