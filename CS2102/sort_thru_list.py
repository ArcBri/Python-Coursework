import csv

flatmodel = 'ADJOINED FLAT'
flattype = '3 ROOM'

with open('resale-flat-prices.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
     if flatmodel == row[7] and flattype == row[2]:

        with open('q1.csv', mode='a', newline='') as csvfile:
         filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
         filewriter.writerow(row)
