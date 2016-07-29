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