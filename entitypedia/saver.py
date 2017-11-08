import csv
import os


class BaseSaver(object):

    def __init__(self):
        pass

    def save(self, obj, filename):
        pass


class CSVSaver(BaseSaver):

    def save(self, obj, filename):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            for result in obj['results']['bindings']:
                row = [result['name']['value'], result['url']['value']]
                writer.writerow(row)