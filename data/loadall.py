import csv
import json, pprint
import time

from app.gmaps import query_place
from app.models import *
from app.models import School
from app.serializers import SchoolLocationsSerializer


def check_short_load(model, short):
    if short and model.objects.all().count() > 100:
        return True
    else:
        return False


def load_subject_enrollment(short=False):
    with open('./data/subject_enrollment.csv', 'rU') as f:
        for line in csv.reader(f):
            year = line[0]
            postcode = line[10]
            subject_name = line[2]
            school_name = str(line[6]).lower().replace(' ', '_').replace('&', 'and')
            year_11_enroll = line[7]
            year_12_enroll = line[8]

            # Loading takes too long
            if '2016' not in year:
                break

            if 'Y' in year_12_enroll:
                year_12_enroll = 1
            elif 'N' in year_12_enroll:
                year_12_enroll = 0

            try:
                school, created = School.objects.get_or_create(name=school_name, postcode=postcode)
                print('[{}] Made school: {}, postcode: {}'.format(year, school_name, postcode))
            except Exception as e:
                print(e)
                print(school_name, postcode)
                continue

            try:
                subject_enrollment, created = SubjectEnrollment.objects.get_or_create(
                    school=school,
                    subject_name=subject_name,
                    year_11_enroll=year_11_enroll,
                    year_12_enroll=year_12_enroll
                )
                print('Made subject enrollment: {}'.format(subject_name))
            except Exception as e:
                print(e)
                print(subject_name, year_11_enroll, year_12_enroll)

            if check_short_load(SubjectEnrollment, short):
                break


def load_attendence(short=False):
    with open('./data/attendence.csv', 'r') as f:
        for line in csv.reader(f):
            break

        for line in csv.reader(f):

            school = line[0].lower().replace(' ', '_').replace('&', 'and')
            year = line[2]
            attendence = line[10].replace('%', '')

            _school = School.objects.filter(name__icontains=school)

            if len(_school) <= 0:
                continue

            _school = _school[0]

            try:
                Attendence.objects.get_or_create(school=_school, year=year, attendence_rate=float(attendence))
                print('Created attendence: {} for {}'.format(attendence, str(_school)))
            except Exception as e:
                print(e)
                print(attendence, year)

            time.sleep(0.0001)

            if check_short_load(Attendence, short):
                break


def load_naplan(short=False):
    with open('./data/naplan.csv', 'r') as f:
        for line in csv.reader(f):
            break

        for line in csv.reader(f):
            school = line[1].lower().replace(' ', '_').replace('&', 'and')

            year5_readingmean = line[12].replace('--', '0').replace('*', '0')
            year5_writingmean = line[13].replace('--', '0').replace('*', '0')
            year5_spellingmean = line[14].replace('--', '0').replace('*', '0')
            year5_grammarmean = line[15].replace('--', '0').replace('*', '0')
            year5_numeracymean = line[16].replace('--', '0').replace('*', '0')

            year9_readingmean = line[22].replace('--', '0').replace('*', '0')
            year9_writingmean = line[23].replace('--', '0').replace('*', '0')
            year9_spellingmean = line[24].replace('--', '0').replace('*', '0')
            year9_grammarmean = line[25].replace('--', '0').replace('*', '0')
            year9_numeracymean = line[26].replace('--', '0').replace('*', '0')

            _school = School.objects.filter(name__icontains=school)

            if len(_school) <= 0:
                continue

            _school = _school[0]

            try:
                Naplan.objects.get_or_create(
                    school=_school,
                    year5_readingmean=year5_readingmean,
                    year5_writingmean=year5_writingmean,
                    year5_spellingmean=year5_spellingmean,
                    year5_grammarmean=year5_grammarmean,
                    year5_numeracymean=year5_numeracymean,

                    year9_readingmean=year9_readingmean,
                    year9_writingmean=year9_writingmean,
                    year9_spellingmean=year9_spellingmean,
                    year9_grammarmean=year9_grammarmean,
                    year9_numeracymean=year9_numeracymean
                )
                print('Made naplan for {}'.format(str(_school)))
            except Exception as e:
                print(e)

            if check_short_load(Naplan, short):
                break


def load_second_language(short=False):
    with open('./data/second_language.csv', 'r') as f:
        for line in csv.reader(f):
            break

        for line in csv.reader(f):

            school = line[0].lower().replace(' ', '_').replace('&', 'and')
            second_language = line[4]

            _school = School.objects.filter(name__icontains=school)

            if len(_school) <= 0:
                continue

            _school = _school[0]

            try:
                SecondLanguage.objects.get_or_create(
                    school=_school,
                    second_language=second_language
                )
                print('Made second language {} to {}'.format(second_language, str(_school)))
            except Exception as e:
                print(e)

            if check_short_load(SecondLanguage, short):
                break


def load_disciplinary(short=False):
    with open('./data/disciplinary.csv', 'r') as f:
        for line in csv.reader(f):
            break

        for line in csv.reader(f):
            school = line[1].lower().replace(' ', '_').replace('&', 'and')

            suspension_type = line[9]
            num_of_incident = line[10]

            _school = School.objects.filter(name__icontains=school)

            if len(_school) <= 0:
                continue

            _school = _school[0]

            try:
                Disciplinary.objects.get_or_create(
                    school=_school,
                    suspension_type=suspension_type,
                    num_of_incident=num_of_incident
                )

            except Exception as e:
                print(e)

            if check_short_load(Disciplinary, short):
                break


def load_long_lat():
    queryset = School.objects.all()

    for query in queryset:
        lat_lng, lat_lng_bounds = query_place(query.name.replace('_', ' ') + ", QLD")
        print(query.name, lat_lng)
        if lat_lng:
            serializer = SchoolLocationsSerializer(instance=query, data=lat_lng, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()


# minlng, maxlng, minlat, maxlat
def load_suburbs(short=False):
    # Create additional CSV
    json_data = open('./data/4cities.json').read()

    my_dict = json.loads(json_data)

    for i in my_dict:
        for key in i:
            try:
                Suburbs.objects.get_or_create(
                    name=key,
                    min_lng=i[key]['northeast']['lng'],
                    min_lat=i[key]['northeast']['lat'],
                    max_lng=i[key]['southwest']['lng'],
                    max_lat=i[key]['southwest']['lat']
                )
                print('[!] Created: {}'.format(key))
            except Exception as e:
                print(e)

    if not short:
        with open('./data/suburbs.csv', 'r') as f:
            for line in csv.reader(f):
                suburb = line[0].lower()

                min_lng = line[1].lower()
                max_lng = line[2].lower()

                min_lat = line[3].lower()
                max_lat = line[4].lower()

                try:
                    Suburbs.objects.get_or_create(
                        name=suburb,
                        min_lat=min_lat,
                        max_lat=max_lat,
                        min_lng=min_lng,
                        max_lng=max_lng
                    )
                    print('Created: {}'.format(suburb))

                except Exception as e:
                    print(e)



def load_all(short=False):
    load_subject_enrollment(short)
    load_attendence(short)
    load_naplan(short)
    load_second_language(short)
    load_disciplinary(short)
    load_suburbs(short)
