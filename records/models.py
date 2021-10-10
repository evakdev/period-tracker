from django.db import models
from django.db.models.deletion import CASCADE
from users.models import User
from tracking.models import Trackable


class Record (models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,related_name='records')
    date = models.DateField()
    log = models.ForeignKey(Trackable,on_delete=CASCADE,related_name='logged')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)