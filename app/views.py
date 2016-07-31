from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from app.gmaps import query_place
from app.models import School, schools_within_bounds, Suburbs
from app.serializers import SchoolLocationsSerializer, BoundsSerializer, \
    SchoolInputSerializer, SchoolSerializer
from app.witty import get_the_query


import time


class MainView(APIView):
    def post(self, request):
        time_start = time.time()
        # Filter by location
        # location = query_place(location)
        # lat1 = lat - 0.05
        # lat2 = lat + 0.05
        # lon1 = lon - 0.05
        # lon2 = lon + 0.05

        # Filter by types
        # Filter by

        # {'school': 'school', 'location': 'brisbane city', 'area': 'numeracy', 'attendance': 'good', 'suspension': 'short'}
        query_data = request.data['query']

        keywords = get_the_query(query_data)

        print(keywords)

        valid_school_ids = [s.id for s in School.objects.all()]

        if type(keywords) is str:
            keywords = {}
            keywords['location'] = request.data['query']

        if 'location' in keywords:
            # Filter by location
            """
            lat_lng, lat_lng_bounds = query_place(keywords['location'])
            formatted_bounds = {'lng1': lat_lng_bounds['southwest']['lng'] - 0.01,
                                'lng2': lat_lng_bounds['northeast']['lng'] + 0.01,
                                'lat1': lat_lng_bounds['southwest']['lat'] - 0.01,
                                'lat2': lat_lng_bounds['northeast']['lat'] + 0.01}
            """
            suburb = Suburbs.objects.filter(name__contains=keywords['location'])

            if len(suburb) > 0:
                suburb = suburb[0]

                print(suburb)

                formatted_bounds = {'lng1': suburb.min_lng - 0.01,
                                    'lng2': suburb.max_lng + 0.01,
                                    'lat1': suburb.min_lat - 0.01,
                                    'lat2': suburb.max_lng + 0.01}

                bounds_serializer = BoundsSerializer(data=formatted_bounds)
                bounds_serializer.is_valid(raise_exception=True)

                queryset = schools_within_bounds(bounds_serializer.validated_data)

                temp_school_id = []
                for q in queryset:
                    temp_school_id.append(q.id)

                valid_school_ids = temp_school_id

        if 'attendance' in keywords:
            # filter attendence

            temp_school_id = []

            for i in valid_school_ids:
                current_naplan = School.objects.get(id=i)

                if 'good' in keywords['attendance']:
                    # If they want good and this school aint good enough, pop
                    if len(current_naplan.attendence_set.all().filter(attendence_rate__gte=85.0)) <= 0:
                        temp_school_id.append(i)

                elif 'high' in keywords['attendance']:
                    if len(current_naplan.attendence_set.all().filter(attendence_rate__gte=95.0)) <= 0:
                        temp_school_id.append(i)

                # Assume
                elif 'bad' in keywords['attendance']:
                    if len(current_naplan.attendence_set.all().filter(attendence_rate__lte=85.0)) <= 0:
                        temp_school_id.append(i)

                # Assume average
                else:
                    if len(current_naplan.attendence_set.all().filter(attendence_rate__lte=100.0)) <= 0:
                        temp_school_id.append(i)

            valid_school_ids = temp_school_id

        if 'area' in keywords:
            temp_school_id = []

            abv_avg = 500
            for i in valid_school_ids:
                current_school = School.objects.get(id=i)

                for current_naplan in current_school.naplan_set.all():

                    if 'numeracy' in keywords['area']:
                        if current_naplan.year9_numeracymean >= abv_avg or current_naplan.year5_numeracymean >= abv_avg:
                            temp_school_id.append(i)

                    elif 'read' in keywords['area']:
                        if current_naplan.year9_readingmean >= abv_avg or current_naplan.year5_readingmean >= abv_avg:
                            temp_school_id.append(i)

                    elif 'writ' in keywords['area']:
                        if current_naplan.year5_writingmean >= abv_avg or current_naplan.year5_writingmean >= abv_avg:
                            temp_school_id.append(i)

                    elif 'spell' in keywords['area']:
                        if current_naplan.year9_spellingmean >= abv_avg or current_naplan.year5_spellingmean >= abv_avg:
                            temp_school_id.append(i)

                    elif 'gram' in keywords['area']:
                        if current_naplan.year9_grammarmean >= abv_avg or current_naplan.year5_grammarmean >= abv_avg:
                            temp_school_id.append(i)

            valid_school_ids = temp_school_id

        if 'suspension' in keywords:

            temp_school_id = []

            total_average = 0

            for i in valid_school_ids:
                current_school = School.objects.get(id=i)

                incidents = 0
                cases = 0
                for current_disciplinary in current_school.disciplinary_set.all():
                    incidents += current_disciplinary.num_of_incident
                    cases += 1

                if cases > 0:
                    average_case = incidents / cases

                    if average_case > 15:
                        continue

                temp_school_id.append(i)

            valid_school_ids = temp_school_id

        if 'language' in keywords:
            language__ = keywords['language']

            temp_school_id = []
            for i in valid_school_ids:
                current_school = School.objects.get(id=i)

                if current_school.secondlanguage_set.all().filter(second_language__contains=language__.lower()):
                    temp_school_id.append(i)

            valid_school_ids = temp_school_id

        queryset = School.objects.filter(id__in=valid_school_ids)
        serializer = SchoolLocationsSerializer(queryset, many=True)

        time_taken = time.time() - time_start
        print(time_taken)
        return Response(data=serializer.data)  # , headers={"Access-Control-Allow-Origin": '*'})

    def get(self, request):
        return render(request, 'index.html')


class SchoolLocationsView(APIView):
    def get(self, request):
        school_set = School.objects.all()
        serializer = SchoolLocationsSerializer(school_set, many=True)
        return Response(data=serializer.data, headers={"Access-Control-Allow-Origin": '*'})


class SchoolView(APIView):
    def get(self, request, school_id):
        input_serializer = SchoolInputSerializer(data={'school': school_id})
        if input_serializer.is_valid(raise_exception=True):
            serializer = SchoolSerializer(
                input_serializer.validated_data['school']
            )
            return Response(data=serializer.data)
