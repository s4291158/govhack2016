import csv, json

def get_subject_enrollment():
    subject_enrollment = {}

    with open('subject_enrollment.csv', 'r') as f:
        lines = f.readlines()[1:]

        i = 0
        for line in lines:
            line = line.replace('\n', '')
            line = line.split(',')
            
            postcode = line[10]            
            subject_name = line[2]
            school_name = line[6]
            year_11_enroll = line[7]
            year_12_enroll = line[8]            

            if postcode in subject_enrollment:
                subject_enrollment[postcode] = {
                    school_name:{
                        subject_name:{
                            'year11': year_11_enroll,
                            'year12': year_12_enroll
                        },
                    },
                    **subject_enrollment[postcode],
                }
            else:
                subject_enrollment[postcode] = {
                    school_name:{
                        subject_name:{
                            'year11': year_11_enroll,
                            'year12': year_12_enroll
                        },
                    },
                }

    return subject_enrollment


def get_attendence():
    attendence_out = {}

    with open('attendence.csv', 'r') as f:
        lines = f.readlines()[1:]
        
        for line in lines:
            line = line.replace('\n', '')
            line = line.split(',')            
            
            school = line[0]
            year = line[2]
            attendence = line[10]            

            if school in attendence:
                attendence_out[school] = {
                    year:{
                        'attendence_rate': attendence,
                    },
                    **attendence[school],
                }
            else:
                attendence_out[school] = {
                    year:{
                        'attendence_rate': attendence,
                    },
                }

    return attendence_out 

def get_naplan():
    naplan_out = {}

    with open('naplan.csv', 'r') as f:
        lines = f.readlines()[1:]

        for line in lines:
            line = line.replace('\n', '')
            line = line.split(',')                
            
            school = line[1]       

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

            naplan_out[school] = {
                'year5_readingmean': year5_readingmean,
                'year5_writingmean': year5_writingmean,
                'year5_spellingmean': year5_spellingmean,
                'year5_grammarmean': year5_grammarmean,
                'year5_numeracymean': year5_numeracymean,

                'year9_readingmean': year9_readingmean,
                'year9_writingmean': year9_writingmean,
                'year9_spellingmean': year9_spellingmean,
                'year9_grammarmean': year9_grammarmean,
                'year9_numeracymean': year9_numeracymean,
            }

    return naplan_out

def get_second_language():
    second_language_out = {}

    with open('second_language.csv', 'r') as f:
        lines = f.readlines()[1:]

        for line in lines:
            line = line.replace('\n', '')
            line = line.split(',')                
            
            school = line[0]     
            second_language = line[4]              

            second_language_out[school] = {
                'second_language': second_language
            }

    return second_language_out