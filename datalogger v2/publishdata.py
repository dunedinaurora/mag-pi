#!usr/bin/python
import dataprocessor_library as dp
import filemanager_library as ofm
import time
import constants as k
import random
import logging
# from constants import mag_readings

# #################################################################################
# Publisher script
# As processing data can take considerable time (up to several seconds) running this
# in sequence with the datalogging may cause bottlenecks, esp when working as a rapid-run
# magnetometer. The simplest solution is to run the processor in parallel with the
# logging script. Managing concurrent python scripts is easily done thru
# appropriate batch/bash scripting
# #################################################################################
RANDOM_SECS = 10                # To randomise the minutes delay
DELAY_SHORT_INTERVAL = 180       # THE DELAY INTERVAL FOR FILE COPYING

# Setup error/bug logging
logging.basicConfig(filename="publisherrors.log", format='%(asctime)s %(message)s')

# #################################################################################
# FUNCTION DEFINITIONS
# Calculate the differences
# #################################################################################
def process_data(input_data_array):
    # If necessary, invert the data so that trends up mean increasing field strength
    data_array = dp.invert_data_array(input_data_array)

    # ###########################################################################
    # Initial filter of data: smoothing, remove transients, etc
    # We're only doing a running average at the moment, but we could add anything,
    # median filter etc...
    # This smoothed data is used to create the magnetogram display files.
    #
    # COMMENT OUT THESE LINES IF WE'RE USING THE DIFFS.CSV FILE TO CREATE OUR DISPLAY FILES
    #
    # ###################################### #####################################
    data_array = dp.median_filter_3values(data_array)
    smoothed_data_array = dp.running_average(data_array) # smooth the array

    # ###########################################################################
    # CReate the differences array and smooth.
    # Do Not Use the smoothed data from previous step. Use original data
    # do several iterations to ensure best appearance.
    # This differences data is used to display rates of change, and minimises the effect
    # of diurnal variation, allowing us to see rapid onsets/changes in the magnetic field.
    # ###########################################################################
    output_diffs = dp.create_diffs_array(data_array)
    for i in range(0,2):
        output_diffs = dp.diffs_running_average(output_diffs)
    ofm.CreateDiffs(output_diffs)  # use output_diffs data


    # ###########################################################
    # create the display files for graphing, using ArraySave.CSV
    #
    # COMMENT OUT THESE LINES IF WE'RE USING THE DIFFS.CSV FILE TO CREATE OUR DISPLAY FILES
    #
    # ###########################################################

    # to get the last 4 hours the split value is mag read frequency * 60 * 4
    splitvalue = k.MAG_READ_FREQ * 60 * 1
    onehrfile = "graphing/dr_01hr.csv"
    ofm.create_hichart_datafile(smoothed_data_array, splitvalue, onehrfile)

    # to get the last 4 hours the split value is mag read frequency * 60 * 4
    splitvalue = k.MAG_READ_FREQ * 60 * 3
    ofm.create_hichart_datafile(smoothed_data_array, splitvalue, k.FILE_4HR)

    # to get the last 24 hours the split value is mag read frequency * 60 * 23
    splitvalue = k.MAG_READ_FREQ * 60 * 23
    ofm.create_hichart_datafile(smoothed_data_array, splitvalue, k.FILE_24HR)

    dp.binnedaverages(data_array) # use original data

    # # ########################################################
    # # create the display files for graphing, using Diffs.csv
    # # use this if we are having major problems with spikes
    # # in final display files
    # # ########################################################
    # smoothed_data_array = dp.readings_from_diffs(output_diffs)
    # ofm.Create24(smoothed_data_array)
    # ofm.Create4(smoothed_data_array)
    # ofm.CreateDiffs(output_diffs) # use output_diffs data
    # datafilters.binnedaverages(smoothed_data_array) # use original data


# #################################################################################
# Main program starts here. Set appropriate delay for tapping into the main arraysave
# file to minimise r/w conflicts
# #################################################################################
while True:
    # how long to perform all the operations
    starttime = time.time()

    mag_readings = []
    try:
        mag_readings = ofm.CreateRawArray()
        # Calculate the processing time
        endtime = time.time()
        processingtime = endtime - starttime
        processingtime = str(processingtime)[:5]
        print("Processing complete. Elapsed time: " + processingtime + " seconds.\n")
        print(str(len(mag_readings)) + " records loaded")
        process_data(mag_readings)
    except:
        print("ERROR: Problem opening file")
        logging.critical(" ERROR: Problem opening file. Unable to create display files")


    timedelay = DELAY_SHORT_INTERVAL + random.randint(0,RANDOM_SECS)
    time.sleep(timedelay)
