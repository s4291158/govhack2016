from django.db import models

from app.gmaps import query_place


class School(models.Model):
    name = models.CharField(max_length=40, unique=True)
    postcode = models.IntegerField()

    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('lat', 'lng')

    def __str__(self):
        return self.name


class SubjectEnrollment(models.Model):
    school = models.ForeignKey(School)

    subject_name = models.CharField(max_length=40)

    year_11_enroll = models.CharField(max_length=40)
    year_12_enroll = models.CharField(max_length=40)

    def __str__(self):
        return self.subject_name


class Attendence(models.Model):
    school = models.ForeignKey(School)

    year = models.IntegerField()
    attendence_rate = models.CharField(max_length=40)

    def __str__(self):
        return self.school


class Naplan(models.Model):
    school = models.ForeignKey(School)

    year5_readingmean = models.IntegerField()
    year5_writingmean = models.IntegerField()
    year5_spellingmean = models.IntegerField()
    year5_grammarmean = models.IntegerField()
    year5_numeracymean = models.IntegerField()

    year9_readingmean = models.IntegerField()
    year9_writingmean = models.IntegerField()
    year9_spellingmean = models.IntegerField()
    year9_grammarmean = models.IntegerField()
    year9_numeracymean = models.IntegerField()

    def __str__(self):
        return self.school


class SecondLanguage(models.Model):
    school = models.ForeignKey(School)

    second_language = models.CharField(max_length=40)

    def __str__(self):
        return self.school


class Disciplinary(models.Model):
    school = models.ForeignKey(School)

    suspension_type = models.CharField(max_length=80)
    num_of_incident = models.IntegerField()

    def __str__(self):
        return self.suspension_type


def schools_within_bounds(coords):
    q = models.Q(
        models.Q(lat__gte=coords['lat1']) &
        models.Q(lat__lte=coords['lat2']) &
        models.Q(lng__gte=coords['lng1']) &
        models.Q(lng__lte=coords['lng2'])
    )
    return School.objects.filter(q)
