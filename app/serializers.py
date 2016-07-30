from django.core.exceptions import ValidationError
from rest_framework import serializers

from app.models import School, SubjectEnrollment, Attendence, Naplan, \
    SecondLanguage, Disciplinary


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


class SubjectEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectEnrollment
        exclude = ('id', 'school')


class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        exclude = ('id', 'school')


class NaplanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naplan
        exclude = ('id', 'school')


class SecondLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondLanguage
        exclude = ('id', 'school')


class DisciplinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplinary
        exclude = ('id', 'school')


class SchoolSerializer(serializers.ModelSerializer):
    subjectenrollment_set = SubjectEnrollmentSerializer(many=True)
    attendence_set = AttendenceSerializer(many=True)
    naplan_set = NaplanSerializer(many=True)
    secondlanguage_set = SecondLanguageSerializer(many=True)
    disciplinary_set = DisciplinarySerializer(many=True)

    class Meta:
        model = School


class SchoolInputSerializer(serializers.Serializer):
    school = serializers.SlugRelatedField(
        slug_field='id',
        queryset=School.objects.all(),
    )
