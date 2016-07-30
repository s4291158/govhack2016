from rest_framework.views import APIView
from rest_framework.response import Response

from app.gmaps import query_place

from django.shortcuts import render

from app.models import School, schools_within_bounds
from app.serializers import SchoolLocationsSerializer, BoundsSerializer


def index_view(request):
    return render(request, 'index.html')


class SchoolLocationsView(APIView):
    def get(self, request):
        school_set = School.objects.all()
        serializer = SchoolLocationsSerializer(school_set, many=True)
        return Response(serializer.data, headers={"Access-Control-Allow-Origin": '*'})

    def post(self, request):
        # TODO: Pass string through Jaimyn's thing

        # Filter by location
        # location = query_place(location)
        # lat1 = lat - 0.01
        # lat2 = lat + 0.01
        # lon1 = lon - 0.01
        # lon2 = lon + 0.01

        # Filter by types

        input_serializer = BoundsSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        school_set = schools_within_bounds(input_serializer.validated_data)
        serializer = SchoolLocationsSerializer(school_set, many=True)
        return Response(serializer.data, headers={"Access-Control-Allow-Origin": '*'})
