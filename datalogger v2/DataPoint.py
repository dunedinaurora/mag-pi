# Datapoint class
__author__ = 'vaughn'

class DataPoint:
    def __init__(self, dateTime, raw_x, raw_y, raw_z):
        self.dateTime = dateTime
        self.raw_x = raw_x
        self.raw_y = raw_y
        self.raw_z = raw_z

    def print_labels(self):
        return "Date/Time (UTC), Raw X, Raw Y, Raw Z"

    def print_values(self):
        return self.dateTime + "," + str(self.raw_x) + "," + str(self.raw_y) + "," + str(self.raw_z)