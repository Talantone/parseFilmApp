from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=511)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title
