import csv

psvfile = 'thing.psv'
outputfile = 'output.csv'
row_num = 0

target = open(outputfile, 'w')

with open(psvfile, 'rt') as psvfile:
    lots_of_data = csv.reader(psvfile, delimiter='|')

    for row in lots_of_data:
        #print(row)
        if "QLD" not in row:
            continue
        line = row[24] + "," + row[28] + ',' + row[29] + '\n'

        target.write(line)
        print(str(row_num))
        row_num = row_num + 1

target.close()