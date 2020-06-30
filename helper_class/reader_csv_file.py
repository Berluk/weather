import csv
from sys import path


class ReaderCsvFile:
    path_csv_file = '/home/lukas/Documents/MyProjects/weather_data.csv'

    @classmethod
    def read_csv_file(cls, row, col):
        with open(cls.path_csv_file, 'r') as csv_file:
            file = csv.reader(csv_file)
            csv_data = [csv_value for csv_value in file]
            return csv_data[row][col]
