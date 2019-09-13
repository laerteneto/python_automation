import csv


def GetCsvData(filename):
    rows = []
    data = open(filename, "r")
    reader = csv.reader(data)
    next(reader)
    for row in reader:
        rows.append(row)
    return rows
