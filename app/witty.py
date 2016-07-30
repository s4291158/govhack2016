from wit import Wit
from localonly.envar import WIT_ACCESS_TOKEN

access_token = WIT_ACCESS_TOKEN
min_confidence = 0.7 #on a scale of 0 = 0% to 1 = 100%

witty = Wit(access_token=access_token)
test = 'What is a school in brisbane city that\'s good at maths, a low short suspension rate, offers the indonesian language and good attendance?'


def get_the_query(phrase):
    processed_phrase = witty.message(phrase)
    processed_data = {}

    for entity in processed_phrase["entities"]: #Loop through every entity found by wit.ai
        if (processed_phrase["entities"][entity][0]["confidence"] < min_confidence): #If the confidence level isn't high enough
            return "unable to recognise one or more phrases"

    if "school" in processed_phrase["entities"]: #If wit.ai found a valid type of school
        if processed_phrase["entities"]["location"][0]["value"] == "school":
            return "school type not specified"
        processed_data["location"] = processed_phrase["entities"]["location"][0]["value"] #Set the location returned

    if "subject" in processed_phrase["entities"]: #If wit.ai found a NAPLAN area/subject
        processed_data["area"] = processed_phrase["entities"]["subject"][0]["value"] #Set the area/subject returned

    if "location" in processed_phrase["entities"]: #If wit.ai found a location
        processed_data["location"] = processed_phrase["entities"]["location"][0]["value"] #Set the location returned

    if "school" in processed_phrase["entities"]: #If wit.ai found a school type
        processed_data["school"] = processed_phrase["entities"]["school"][0]["value"] #Set the school type returned

    else: #If no school type was found
        return "no school type was recognised"

    if "suspension" in processed_phrase["entities"]: #If wit.ai found a suspension type
        processed_data["suspension"] = processed_phrase["entities"]["suspension"][0]["value"] #Set the suspension type returned

    if "attendance" in processed_phrase["entities"]: #If wit.ai found an attendance request
        processed_data["attendance"] = processed_phrase["entities"]["attendance"][0]["value"] #Set the suspension type returned

    if "language" in processed_phrase["entities"]: #If wit.ai found an attendance request
        processed_data["language"] = processed_phrase["entities"]["language"][0]["value"] #Set the suspension type returned

    return processed_data

#Use it like this get_the_query(phrase_you_want_to_parse)

# get_the_query(phrase_you_want_to_parse)

# example input: 'What is a school in brisbane city that\'s good at maths, a low short suspension rate, offers the indonesian language and good attendance?'
# example output: {'school': 'school', 'location': 'brisbane city', 'area': 'numeracy', 'attendance': 'good', 'suspension': 'short'}
#                             ^ an output of school means it wasn't specified