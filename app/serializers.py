from rest_framework import serializers

from app.models import School


class SchoolLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'lat', 'lng')
