from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import School, schools_within_bounds
from app.serializers import SchoolLocationsSerializer, BoundsSerializer


class SchoolLocationsView(APIView):
    def get(self, request):
        school_set = School.objects.all()
        serializer = SchoolLocationsSerializer(school_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        input_serializer = BoundsSerializer(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            school_set = schools_within_bounds(input_serializer.validated_data)
            serializer = SchoolLocationsSerializer(school_set, many=True)
            return Response(serializer.data)
