import csv

csvfile = 'output.csv'
outputfile = 'suburbs.csv'
row_num = 0
suburbs = {}

target = open(outputfile, 'w')

with open(csvfile, 'rt') as things:
    lots_of_data = csv.reader(things, delimiter=',')

    for row in lots_of_data:
        if row[0] not in suburbs:
            suburbs[row[0]] = {
                 'min_lat': row[2],
                 'max_lat': row[2],
                 'min_lng': row[1],
                 'max_lng': row[1]}

        else:
            if row[1] < suburbs[row[0]]["min_lng"]:
                suburbs[row[0]]["min_lng"] = row[1]

            if row[1] > suburbs[row[0]]["max_lng"]:
                suburbs[row[0]]["max_lng"] = row[1]

            if row[2] < suburbs[row[0]]["min_lat"]:
                suburbs[row[0]]["min_lat"] = row[2]

            if row[2] > suburbs[row[0]]["max_lat"]:
                suburbs[row[0]]["max_lat"] = row[2]

print(suburbs)

for each in suburbs:
    line = each + "," + suburbs[each]["min_lng"] + "," + suburbs[each]["max_lng"] + ',' + suburbs[each]["min_lat"] + "," + suburbs[each]["max_lat"] + '\n'
    target.write(line)

#target.write()
target.close()