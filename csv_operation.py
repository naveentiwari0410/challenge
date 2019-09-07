import csv

class CSVOperation():
    def __init__(self, filename, header):
        self.filename = filename
        self.header = header

    def write(self, data):
        with open(self.filename, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header)
            writer.writeheader()
            writer.writerows(data)