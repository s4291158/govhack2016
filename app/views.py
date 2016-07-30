from rest_framework.views import APIView
from rest_framework.response import Response

from app.witty import get_the_query
from app.gmaps import query_place

from django.shortcuts import render

from app.models import School, schools_within_bounds
from app.serializers import SchoolLocationsSerializer, BoundsSerializer, \
    SchoolInputSerializer, SchoolSerializer


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
        # lat1 = lat - 0.05
        # lat2 = lat + 0.05
        # lon1 = lon - 0.05
        # lon2 = lon + 0.05

        # Filter by types
        # Filter by

        # {'school': 'school', 'location': 'brisbane city', 'area': 'numeracy', 'attendance': 'good', 'suspension': 'short'}
        query_data = request.POST['query']
        query_respond = get_the_query(query_data)

        # Focusing on area, location, and attendence
        query_set = School.objects.all()

        if 'location' in query_data:
            # Filter by location
            location_filter_data = {}
            query_set.objects.filter()

        input_serializer = BoundsSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        school_set = schools_within_bounds(input_serializer.validated_data)
        serializer = SchoolLocationsSerializer(school_set, many=True)
        return Response(serializer.data, headers={"Access-Control-Allow-Origin": '*'})


class SchoolView(APIView):
    def get(self, request, school_id):
        input_serializer = SchoolInputSerializer(data={'school': school_id})
        if input_serializer.is_valid(raise_exception=True):
            serializer = SchoolSerializer(
                input_serializer.validated_data['school']
            )
            return Response(serializer.data)
