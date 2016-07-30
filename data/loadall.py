import csv
import time
from app.models import *

def load_subject_enrollment():

    with open('./data/subject_enrollment.csv', 'rU') as f:
        for line in csv.reader(f):
            year = line[0]
            postcode = line[10]
            subject_name = line[2]
            school_name = str(line[6]).lower().replace(' ', '_').replace('&', 'and')
            year_11_enroll = line[7]
            year_12_enroll = line[8]

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

def load_attendence():
    with open('./data/attendence.csv', 'r') as f:
        for line in csv.reader(f):
            break

        for line in csv.reader(f):

            school = line[0].lower().split(' ')
            year = line[2]
            attendence = line[10]


            _school = School.objects.filter(name__contains=school[0])[0]

            if len(_school) <= 0:
                continue

            try:
                Attendence.objects.get_or_create(school=_school, year=year, attendence_rate=attendence)
                print('Created attendence: {}'.format(attendence))
            except Exception as e:
                print(e)
                print(attendence, year)

            time.sleep(0.0001)

def load_naplan():
    with open('./data/naplan.csv', 'r') as f:
        for line in csv.reader(f):
            break

        for line in csv.reader(f):

            school = line[1].lower().split(' ')

            year5_readingmean = line[12]
            year5_writingmean = line[13]
            year5_spellingmean = line[14]
            year5_grammarmean = line[15]
            year5_numeracymean = line[16]

            year9_readingmean = line[22]
            year9_writingmean = line[23]
            year9_spellingmean = line[24]
            year9_grammarmean = line[25]
            year9_numeracymean = line[26]

            _school = School.objects.filter(name__contains=school[0])[0]

            if len(_school) <= 0:
                continue

            try:
                Naplan.objects.get_or_create(
                    school=_school,
                    year5_readingmean= year5_readingmean,
                    year5_writingmean= year5_writingmean,
                    year5_spellingmean= year5_spellingmean,
                    year5_grammarmean= year5_grammarmean,
                    year5_numeracymean= year5_numeracymean,

                    year9_readingmean= year9_readingmean,
                    year9_writingmean= year9_writingmean,
                    year9_spellingmean= year9_spellingmean,
                    year9_grammarmean= year9_grammarmean,
                    year9_numeracymean= year9_numeracymean
                )
                print('Made naplan')
            except Exception as e:
                print(e)




def load_second_language():

    with open('./data/second_language.csv', 'r') as f:
        for line in csv.reader(f):
            break

        for line in csv.reader(f):

            school = line[0].lower().split()
            second_language = line[4]

            _school = School.objects.filter(name__contains=school[0])[0]

            if len(_school) <= 0:
                continue

            try:
                SecondLanguage.objects.get_or_create(
                    school=_school,
                    second_language=second_language
                )
                print('Made second language {}'.format(second_language))
            except Exception as e:
                print(e)



def load_disciplinary():

    with open('./data/disciplinary.csv', 'r') as f:
        for line in csv.reader(f):
            break

        for line in csv.reader(f):
            school = line[1].lower().split(' ')

            suspension_type = line[9]
            num_of_incident = line[10]

            _school = School.objects.filter(name__contains=school[0])[0]

            if len(_school) <= 0:
                continue

            try:
                Disciplinary.objects.get_or_create(
                    school=_school,
                    suspension_type=suspension_type,
                    num_of_incident=num_of_incident
                )

            except Exception as e:
                print(e)




def load_all():
    load_subject_enrollment()
    load_attendence()
    load_naplan()
    load_second_language()
    load_disciplinary()
