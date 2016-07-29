from django.db import models


class School(models.Model):
    name = models.CharField(max_length=40, unique=True)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        unique_together = ('lat', 'lng')

    def __str__(self):
        return self.name
