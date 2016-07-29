from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import School
from app.serializers import SchoolLocationSerializer


class SchoolLocationView(APIView):
    def get(self, request):
        school_set = School.objects.all()
        serializer = SchoolLocationSerializer(school_set, many=True)
        return Response(serializer.data)
