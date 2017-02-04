# Datapoint class
__author__ = 'vaughn'

class DataPoint:
    def __init__(self, dateTime, raw_f):
        self.dateTime = dateTime
        self.raw_f = raw_f
        # self.raw_y = raw_y
        # self.raw_z = raw_z

    def print_labels(self):
        return "Date/Time (UTC), Raw F"

    def print_values(self):
        return self.dateTime + "," + str(self.raw_f)