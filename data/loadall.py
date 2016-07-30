import csv
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

            school = line[0].lower().split(' ')
            year = line[2]
            attendence = line[10].replace('%', '')

            _school = School.objects.filter(name__contains=school[0])

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
            school = line[1].lower().split(' ')

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

            _school = School.objects.filter(name__contains=school[0])

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

            school = line[0].lower().split()
            second_language = line[4]

            _school = School.objects.filter(name__contains=school[0])

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
            school = line[1].lower().split(' ')

            suspension_type = line[9]
            num_of_incident = line[10]

            _school = School.objects.filter(name__contains=school[0])

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
        ret = query_place(query.name.replace('_', ' '))
        ret.pop('postal')
        serializer = SchoolLocationsSerializer(instance=query, data=ret, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


def load_all(short=False):
    load_subject_enrollment(short)
    load_attendence(short)
    load_naplan(short)
    load_second_language(short)
    load_disciplinary(short)
    load_long_lat()
