import DataPoint
import constants as k
import os.path
import logging
import math
from decimal import Decimal, getcontext
import re
import filemanager_library as ofm

__author__ = 'vaughn'
getcontext().prec = 5

# #################################################################################
# Data processing script
# this library is for anything that crunches and manipulates data
#
# #################################################################################

# #################################################################################
# This function is used to build up an array of readings from the diffs file. We might do this if for
# some reason the median filter is not catching spikes, or we have consecutive readings (2 - 5) of spiking.
# The createDiffs function, should have rejected these values.
# #################################################################################
def readings_from_diffs(diffsarray):
    # set up the return array and x,y, and z storage values
    outputarray = []
    f_value = 0.0

    # for each datapoint in the diffs array...
    for datapoints in diffsarray:
        # create cumulative values that will become our "readings"
        f_value = f_value + float(datapoints.raw_f)

        # create a datapoint with the new values. Append to return array
        appenddata = DataPoint.DataPoint(datapoints.dateTime, f_value)
        outputarray.append(appenddata)

    # return array
    return outputarray

# #################################################################################
# data inverter
# If necessary, invert the data so that trends up mean increasing field strength
# #################################################################################
def invert_data_array(data_array):
    returnarray = []
    for i in range(0, len(data_array)):
        f = Decimal(data_array[i].raw_f) * k.FIELD_CORRECTION
        dp = DataPoint.DataPoint(data_array[i].dateTime, f)
        returnarray.append(dp)

    return returnarray

# #################################################################################
# Calculate the differences
# This function will create an array of differences
# this can be used to create a new display array of relative readings, that do
# not have nose spikes in them
# #################################################################################
def create_diffs_array(readings_array):
    spike_counter = 0
    diffsarray = []
    counterbit = 0

    if len(readings_array) > 2:
        for i in range (1, len(readings_array)):
            counterbit = 0
            diff_x = (Decimal(readings_array[i].raw_x) - Decimal(readings_array[i-1].raw_f))
            # Each IF statement checks to see if reading exceeds the spike value. If it does
            # then we change the reading to zero. We trip the counterbit and at the end of the
            # data read incr the spike counter
            if math.sqrt(math.pow(diff_f,2)) > k.NOISE_SPIKE:
                diff_f = 0
                counterbit = 1

            dp = DataPoint.DataPoint(readings_array[i].dateTime,diff_f)
            diffsarray.append(dp)

            if counterbit == 1:
                spike_counter = spike_counter + 1
                counterbit = 0
    else:
        dp = DataPoint.DataPoint("0000-00-00 00:00:00",0)
        diffsarray.append(dp)

    return diffsarray


# #################################################################################
# Datafilters
# THis script may just be merged into the dataprocessor script
#
# #################################################################################

# #################################################################################
# Median filter based on 3 values
#
# #################################################################################
def median_filter_3values(arraydata):
    outputarray = []

    for i in range(1,len(arraydata)-1):
        xlist = []


        for j in range(-1,2):    # -1, 0, 1
            k = i + j
            xlist.append(arraydata[k].raw_x)

        xlist.sort()

        dp = DataPoint.DataPoint(arraydata[i].dateTime, xlist[1])

        outputarray.append(dp)

    return outputarray


# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
#
# we will divide this number evenly so our average represents the midpoint of these
# readings.
# #################################################################################
def diffs_running_average(input_array):
    getcontext().prec = 5
    displayarray = []
    timeinterval = 4 # minutes

    # This figure MUST be an even number. Check your constants.
    AVERAGING_TIME = int(timeinterval * k.MAG_READ_FREQ)
    AVERAGING_TIME_HALF = int(AVERAGING_TIME / 2)

    # NOW average the cumulative array, smooth out the blips
    if len(input_array) > AVERAGING_TIME:
        for i in range(AVERAGING_TIME_HALF, len(input_array) - AVERAGING_TIME_HALF):
            fvalue = 0

            # This is where we average for the time i before and after i.
            for j in range(0, AVERAGING_TIME):
                xvalue = fvalue + Decimal(input_array[(i - AVERAGING_TIME_HALF) + j].raw_f)

            xvalue = Decimal(fvalue / AVERAGING_TIME)

            displaypoint = DataPoint.DataPoint(input_array[i].dateTime, fvalue)
            displayarray.append(displaypoint)

    else:
        displayarray = input_array

    return displayarray
# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
#
# we will divide this number evenly so our average represents the midpoint of these
# readings.
# #################################################################################
def running_average(input_array):
    getcontext().prec = 5
    displayarray = []

    # This figure MUST be an even number. Check your constants.
    AVERAGING_TIME = int(k.MAG_RUNNINGAVG_COUNT)
    AVERAGING_TIME_HALF = int(AVERAGING_TIME / 2)

    # NOW average the cumulative array, smooth out the blips
    if len(input_array) > AVERAGING_TIME:
        for i in range(AVERAGING_TIME_HALF, len(input_array) - AVERAGING_TIME_HALF):
            fvalue = Decimal(0)

            # This is where we average for the time i before and after i.
            for j in range(0, AVERAGING_TIME):
                xvalue = fvalue + Decimal(input_array[(i - AVERAGING_TIME_HALF) + j].raw_f)

            xvalue = Decimal(fvalue / AVERAGING_TIME)

            displaypoint = DataPoint.DataPoint(input_array[i].dateTime, fvalue)
            displayarray.append(displaypoint)

    else:
        displayarray = input_array

    return displayarray

# #################################################################################
# Create binned minutely averages
# to be used for experimental data/sensor merge project
# #################################################################################
def binnedaverages(readings):
    # Get each datapoint to print out it's values. Use re to split this on spaces, commas, and semi colons.
    # ['2016-05-08', '03', '34', '37.61', '6.12', '-8.24', '62.82', '0', '0', '0']
    fAvg = Decimal(0)

    binnedvalues = []
    counter = Decimal(0)

    # Open the readings array
    for j in range(0, len(readings)-1):
        # Get the first datapoint from the array, so we get the current minute...
        # dpvalues = re.split(r'[\s,:]', readings[j].dateTime)
        dpvalues = re.split(r'[\s,:]', readings[j].print_values())
        nowminute = dpvalues[2]
        datetime = dpvalues[0] + " " + dpvalues[1] + ":" + nowminute
        print(str(datetime))

        # get the value for the next minute
        dpvalues1 = re.split(r'[\s,:]', readings[j + 1].print_values())
        nextminute = dpvalues1[2]

        if nowminute == nextminute:
            xAvg = fAvg + Decimal(dpvalues[4])
            counter = counter + 1

            # print(nowminute + " " + str(xAvg))
        elif nowminute != nextminute:
            xAvg = fAvg / counter

            dp = DataPoint.DataPoint(datetime, fAvg)
            binnedvalues.append(dp)

            fAvg = 0
            counter = 0
        else:
            counter = 0

    # WRITE OUT to binned file.
    try:
        # print("Write to file " + dp.print_values())
        with open (k.FILE_BINNED_MINS, 'w') as b:
            for dataObjects in binnedvalues:
                # dataObjects.print_values()
                b.write(dataObjects.print_values() + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + k.FILE_BINNED_MINS)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_BINNED_MINS)

