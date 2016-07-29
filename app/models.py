from django.db import models


class School(models.Model):
    name = models.CharField(max_length=40)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name
