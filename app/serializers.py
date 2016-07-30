from django.core.exceptions import ValidationError
from rest_framework import serializers

from app.models import School


class SchoolLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name', 'lat', 'lng')


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


class SchoolInputSerializer(serializers.Serializer):
    school = serializers.SlugRelatedField(
        slug_field='id',
        queryset=School.objects.all(),
    )


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
