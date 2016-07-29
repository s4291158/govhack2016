from django.db import models


class School(models.Model):
    name = models.CharField(max_length=40, unique=True)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        unique_together = ('lat', 'lng')

    def __str__(self):
        return self.name


def schools_within_bounds(coords):
    q = models.Q(
        models.Q(lat__gte=coords['lat1']) &
        models.Q(lat__lte=coords['lat2']) &
        models.Q(lng__gte=coords['lng1']) &
        models.Q(lng__lte=coords['lng2'])
    )
    return School.objects.filter(q)
