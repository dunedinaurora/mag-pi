__author__ = 'vaughn'

# Constants
MAG_READ_FREQ = 6         # how often the magnetometer sends data per minute
MAG_RUNNINGAVG_COUNT = 6   # The number of readings "wide" the averaging window is. EVEN NUMBER
NOISE_SPIKE = 50          # spike threshold for G857 readings
FIELD_CORRECTION = 1        # if the field is increasing in strength, the values should go up, and vica versa
STATION_ID = "Otago Museum."

# Files
PATH_LOGS = 'logs/'
PATH_GRAPHING = 'graphing/'
FILE_ROLLING = 'ArraySave.csv'
FILE_24HR = PATH_GRAPHING + "G857_24hr.csv"
FILE_4HR = PATH_GRAPHING + "G857_04hr.csv"
FILE_4DIFFS = PATH_GRAPHING + "G857_diffs.csv"
FILE_ERRORLOG = "Errors.log"
FILE_BINNED_MINS = PATH_GRAPHING + STATION_ID + "1minbins.csv"

lastdatavalue = 0

# Comm port parameters - uncomment and change one of the portNames depending on your OS
portName = 'Com11' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS or Linux
baudrate = 9600
bytesize = 8
parity = 'N'
stopbits = 1
timeout = 60
xonxoff = False
rtscts = True
writeTimeout = None
dsrdtr = False
interCharTimeout = None
