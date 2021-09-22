from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Trackable(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='trackables' ,null=True)

    def __str__(self):
        return self.name


class Cycle(models.Model):
    first = models.DateField()
    last = models.DateField(null=True)
    order_num = models.IntegerField()

    @property
    def duration(self):
        if self.last:
            return int(self.last - self.first)
    
    def __str__(self):
        return f'Cycle {self.order_num}'



class Day(models.Model):
    date = models.DateField()
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE,related_name='days', null=True)
    logs = models.ManyToManyField(Trackable)

    def __str__(self):
        return self.date