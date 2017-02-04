#!/usr/bin/python
import DataPoint
import constants as k
import filemanager_library
import serial
import datetime
import logging
import os
import re
import time
# from constants import mag_readings

__author__ = 'Vaughn Malkin'
__version__ = "1.8.0"


# *****************************************************************************************
# This script logs data from a serial port. The data format is given below. This data is 
# appended to an array of the last 24 hours, and saved to a logfile. The datetime is UTC.
# In order to faciliate read speed from the com port, no other processing of data happens 
# in this script. 
# 
# *****************************************************************************************

# *****************************************************************************************
# B E G I N   F U N C T I O N   D E F I N I T I O N S
# *****************************************************************************************

# Check serial data is 3 positive or negative comma separated decimal numbers.
def CheckData(logDataToAdd):
    # Checking here.
    if re.match(r'\A-?\d+(\.\d+)?[,]-?\d+(\.\d+)?[,]-?\d+(\.\d+)?\Z',logDataToAdd):
        LogRawMagnetometerData(logDataToAdd)
    else:
        print("Garbage data from Magnetometer: " + logDataToAdd)
        logging.warning("WARNING: Garbage data from Magnetometer: " + logDataToAdd)

# *****************************************************************************************
# FUNCTION - create a rotating log for data based on date
# *****************************************************************************************
def LogRawMagnetometerData(logDataToAdd):
    # get current datetime based on system clock. NOT UTC by default
    # dt = datetime.datetime.now()

    # dt as UTC
    dt = datetime.datetime.utcnow()

    # a formatted Datetime object for recording inside the logfile
    logdate = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

    # LogdatatoAdd is 3 comma sep values. Split them on the comma into a list thing.
    lg = logDataToAdd.split(",")

    # Create the DataPoint object, pass in the datetime and the 3 list values
    dp = DataPoint.DataPoint(str(logdate), lg[0], lg[1], lg[2])

    # DP is added to array.
    filemanager_library.AppendDataPoint(dp, mag_readings)

    # Save the array to the ArraySave.csv file loaded at the beginning
    filemanager_library.SaveRawArray(mag_readings)

    ###############################################
    # Logdata to be appended to current 24 hr file
    ###############################################
    # Grab the latest entry from th readings array with calculated values.
    # By this point readings will have the differences added.
    logData = mag_readings[len(mag_readings) - 1].print_values()

    # RAW log file name is created now. Get the date part of dt, add file suffix
    RawlogName = str(dt.date())
    RawlogName = k.PATH_LOGS + RawlogName + '.csv'

    # If the logfile exists append the datapoint
    if os.path.isfile(RawlogName):
        try:
            with open (RawlogName,'a') as f:
                f.write(logData + '\n')
                # print("Data logged ok. Array Size: " + str(len(readings)))
        except IOError:
            print("WARNING: There was a problem accessing the current logfile: " + RawlogName)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + RawlogName)

    # ELSE add the header to the file because it is new
    else:
        try:
            with open (RawlogName,'a') as f:
                f.write(dp.print_labels() + '\n')

            print("Creating new logfile")
        except IOError:
            print("WARNING: There was a problem accessing the current logfile: " + RawlogName)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + RawlogName)

    # If applicable, pass the datapoint to the MYSQL database routine.

# *****************************************************************************************
# E N D   F U N C T I O N   D E F I N I T I O N S
# *****************************************************************************************


# *****************************************************************************************
# B E G I N   M A I N
# *****************************************************************************************

print("Pything Data Logger")
print("(c) Vaughn Malkin 2015, 2016, 2017")
print("Version " + __version__)
print(" ")
print("YOU MUST USE PYTHON VER 3 FOR THIS CODE")

# Setup error/bug logging
logging.basicConfig(filename=k.FILE_ERRORLOG, format='%(asctime)s %(message)s')

# setup file paths
# Set up file structure for Data logs. Linux systems might need use of the mode arg to set correct permissions.
try:
    os.makedirs(k.PATH_LOGS)
    print("Logfile directory created.")
except:
    if not os.path.isdir(k.PATH_LOGS):
        print("Unable to create log directory")
        logging.critical("CRITICAL ERROR: Unable to create logs directory")
try:
    os.makedirs(k.PATH_GRAPHING)
    print("Graphing file directory created.")
except:
    if not os.path.isdir(k.PATH_LOGS):
        print("Unable to create Graphing file directory")
        logging.critical("CRITICAL ERROR: Unable to create Graphing file directory")

# setup array for datapoints
mag_readings = []

# Set up the infernal com port. Add a TRY-CATCH to deal with possible com port problems
try:
    com = serial.Serial(k.portName,k.baudrate,k.bytesize,k.parity,k.stopbits,k.timeout,k.xonxoff,k.rtscts,k.writeTimeout,k.dsrdtr,k.interCharTimeout)
except serial.SerialException:
    print("CRITICAL ERROR: Com port not responding. Please check parameters")
    logging.critical("CRITICAL ERROR: Unable to open com port. Please check com port parameters and/or hardware!!")

# Print out the port name for the edification of all concerned
print("Port is: ", com.name)

# Initialise array from savefile if possible, otherwise new array
mag_readings = filemanager_library.CreateRawArray()

# *****************************************************************************************
# MAIN LOOP. Only the End of Days will stop this program.
# Actually we need some kind of timeout on this.
# *****************************************************************************************
while True:
    logData = com.readline()                    # logData is a byte array, not a string at this point
    logData = str(logData,'ascii').strip()      # convert the byte array to string. strip off unnecessary whitespace

    # how long to perform all the operations for each read of the magnetometer?
    starttime = time.time()

    # Process the magnetometer data
    CheckData(logData)

    # Calculate the processing time
    endtime = time.time()
    processingtime = endtime - starttime
    processingtime = str(processingtime)[:5]

    # User output displayed on console
    if len(mag_readings) > 1:
        print("Time to process : " + processingtime + "\t\t" + " Magnetometer Data: " + mag_readings[len(mag_readings)-1].print_values() + "\t\t" + str(len(mag_readings)) + " records")
