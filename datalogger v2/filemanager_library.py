import constants as k
import os.path
import logging
import DataPoint

__author__ = 'Meepo'

# ###################################################################
# FileManager
# This library is for reading from and writing to files
#
# ###################################################################

def CreateDiffs(diffsArray):
    try:
        os.remove(k.FILE_4DIFFS)
    except OSError:
        print("WARNING: could not delete " + k.FILE_4DIFFS)
        logging.warning("WARNING: File IO Exception raised - could not delete: " + k.FILE_4DIFFS)

    try:
        with open (k.FILE_4DIFFS,'a') as f:
            f.write("Date/Time (UTC), Ultra-smoothed Differences" + "\n")
            for datapoints in diffsArray:
                f.write(datapoints.dateTime + "," + str(datapoints.raw_x) + "," + str(datapoints.raw_y) + "," + str(datapoints.raw_z) + '\n')
                #f.write(datapoints.dateTime + "," + str(datapoints.raw_x)  + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + k.FILE_4DIFFS)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_4DIFFS)


# ############################################################
# Create display file for Highcharts
# ############################################################
def create_hichart_datafile(readingsArray, splitvalue, filename):

    displayList = readingsArray[(len(readingsArray) - splitvalue):]

    try:
        os.remove(filename)
    except OSError:
        print("WARNING: could not delete " + filename)
        logging.warning("WARNING: File IO Exception raised - could not delete: " + filename)

    try:
        with open(filename, 'a') as f:
            f.write("Date/Time (UTC), Reading" + "\n")
            for datapoints in displayList:
                f.write(datapoints.dateTime + "," + str(datapoints.raw_x) + "," + str(datapoints.raw_y) + "," + str(datapoints.raw_z) + '\n')
                # f.write(datapoints.dateTime + "," + str(datapoints.raw_x) + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + filename)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + filename)


# #################################################################################
# Create the raw datapoint array from the save file
# #################################################################################
def CreateRawArray():
    readings = []
    # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
    if os.path.isfile(k.FILE_ROLLING):
        with open(k.FILE_ROLLING) as e:
            for line in e:
                line = line.strip() # remove any trailing whitespace chars like CR and NL
                values = line.split(",")
                # See the datapoint object/constructor for the current values it holds.
                dp = DataPoint.DataPoint(values[0], values[1], values[2], values[3])
                readings.append(dp)
        print("Array loaded from file. Size: " + str(len(readings)) + " records")
    else:
        print("No save file loaded. Using new array.")

    return readings

# #################################################################################
# Save the raw datapoint array to the save file
# #################################################################################
def SaveRawArray(readings):
    # export array to array-save file
        try:
            with open (k.FILE_ROLLING, 'w') as w:
                for dataObjects in readings:
                    w.write(dataObjects.print_values() + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + k.FILE_ROLLING)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_ROLLING)

# #################################################################################
#  Append a new datapoint
# #################################################################################
def AppendDataPoint(datapoint, readingsArray):
    # Append the datapoint to the array. Prune off the old datapoint if the array is 24hr long
    if(len(readingsArray) < k.MAG_READ_FREQ * 60 * 24):
        readingsArray.append(datapoint)
    else:
        readingsArray.pop(0)
        readingsArray.append(datapoint)