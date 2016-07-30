from django.core.exceptions import ValidationError

from rest_framework import serializers

from app.gmaps import query_place
from app.models import School


def load_long_lat():
    queryset = School.objects.all()

    for query in queryset:
        ret = query_place(query.postcode)
        ret.pop('postal')
        serializer = SchoolLocationsSerializer(instance=query, data=ret, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class SchoolLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'lat', 'lng')


class BoundsSerializer(serializers.Serializer):
    lat1 = serializers.FloatField()
    lng1 = serializers.FloatField()
    lat2 = serializers.FloatField()
    lng2 = serializers.FloatField()

    def validate(self, attrs):
        if attrs['lat1'] > attrs['lat2']:
            raise ValidationError(
                'lat2 should be larger than or equal to lat1.'
            )
        elif attrs['lng1'] > attrs['lng2']:
            raise ValidationError(
                'lng2 should be larger than or equal to lng1.'
            )

        return attrs
