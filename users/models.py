
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


    
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
