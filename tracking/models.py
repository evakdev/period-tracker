
from django.db.models.deletion import CASCADE
from users.models import User


from tracking.exceptions import NameNotUniqueInCategory
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Flow(models.Model):
    user = models.OneToOneField(User,on_delete=CASCADE,related_name='flow')

class Trackable(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='trackables', null=True)
    related_flow = models.ForeignKey(Flow, on_delete=CASCADE,related_name='trackables', null=True,blank=True)
    
    def __str__(self):
        return self.name

    def assign_category(self,category_to_be):
        if not self.name_is_unique_in_category(category_to_be.name):
            raise NameNotUniqueInCategory  
        self.category = category_to_be
        return category_to_be
        
    