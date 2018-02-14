import csv


def read_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for line in reader:
            yield line
            #entity, label = line
            #yield entity, label
