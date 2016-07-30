from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from app.models import schools_within_bounds, School

from model_mommy import mommy
from random import randrange


class SchoolLocationsTests(APITestCase):
    def setUp(self):
        self.url = reverse('school_locations')
        for _ in range(randrange(1, 10)):
            mommy.make('School')

    def test_get_ok(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), School.objects.all().count())

    def test_post_ok(self):
        coords = {
            'lat1': randrange(-10, 0),
            'lat2': randrange(0, 10),
            'lng1': randrange(-10, 0),
            'lng2': randrange(0, 10)
        }
        response = self.client.post(self.url, data=coords)

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except AssertionError as e:
            e.args += (response.data,)
            raise e
        self.assertEqual(len(response.data), schools_within_bounds(coords).count())
