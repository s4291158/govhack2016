from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import School, schools_within_bounds
from app.serializers import SchoolLocationsSerializer, BoundsSerializer

from app.gmaps import query_place

class SchoolLocationsView(APIView):
    def get(self, request):
        school_set = School.objects.all()
        serializer = SchoolLocationsSerializer(school_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        # todo: pass through jaimyn's wit.ai thingy

        # for now assume its a location
        return Response(data=query_place(request.data['location']))
