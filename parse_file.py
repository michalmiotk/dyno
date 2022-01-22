import csv


def get_values_from_file(filename):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        values = []
        for row in spamreader:  
            for value in row:
                values.append(int(value))

        return values
