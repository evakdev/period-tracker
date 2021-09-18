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
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=128)

    def __str__(self):
        return self.name


class Cycle(models.Model):
    first = models.DateField()
    last = models.DateField(null=True)
    duration = models.PositiveIntegerField(null=True)
    idnum = models.PositiveIntegerField()


class Day(models.Model):
    date = models.DateField()
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, null=True)
    logs = models.ManyToManyField(Trackable)
