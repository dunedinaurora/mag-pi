# #################################################################################
# This python library is to provide functions to access a database
# #################################################################################
import mysql.connector as mariadb
import logging
import re
# import connect.py

# #################################################################################
# Function Definitions
# #################################################################################
def StoreInDB(dp):
    # data is at positions 2
    timestamp = dp.dateTime
    dataF = dp.raw_f

    # The ID number for POrtobello as stored in the Database
    idStation = 1

    # When building up query strings, use the mariaDBs pyformat method as it will ensure strings stay as strings, not escape
    # codes or anything horrid...
    # http://stackoverflow.com/questions/7929364/python-best-practice-and-securest-to-connect-to-mysql-and-execute-queries
    # eg: cursor.execute("SELECT spam FROM eggs WHERE lumberjack = %(jack)s", {'jack': lumberjack})
    # queryString = "insert into DataXYZ (timestamp, idStationxyz, dataX, dataY, dataZ) values ('2015-08-18 04:50:39.181648','1',11141,-19302,-47574)"
    # NOTE: The whole DB shebang has been moved in here as it's just easier to do the correct building of the script to prevent SQL injects this way.
    try:
        dbConnection = mariadb.connect(host='127.0.0.1', port=3307,user='User', password='Password', database='database')
        print("INFO: Connect to remote DB ok.")

        # Instantiate the cursor object to interact with the database
        cursor = dbConnection.cursor()

        # send query
        # The result of the query is stored in a list called "cursor." To test the result you can print
        # it with a simple for loop, but for better formatting use Python's string formatting method:
        try:
            # http://stackoverflow.com/questions/7929364/python-best-practice-and-securest-to-connect-to-mysql-and-execute-queries
            cursor.execute("insert into DataF (timestamp, dataF, idStationf) values (%(timestamp)s, %(dataF)s, %(idStationxyz)s)",\
                           {'timestamp': timestamp, 'dataF':dataF, 'idStationxyz': idStation})
            dbConnection.commit() # Commit the query to the DB, not enable by default

        except mariadb.Error as error:
            errorMsg = "SQL Error: {}".format(error)
            print(errorMsg) # SQL errors will be displayed on console. Probably need to log this.
            logging.error("ERROR: MySQL " + errorMsg)
            dbConnection.rollback() # rollback the query

        except:
            errorMsg = "ERROR: Unhandled MySQL exception error!"
            print(errorMsg)
            logging.warning(errorMsg)
            dbConnection.rollback() # rollback the query

        # CLOSE the connection to the DB. We don't want open connections dangling everywhere now, do we?
        dbConnection.close()

    except mariadb.Error as error:
        errorMsg = "ERROR: MySQL connection error " + str(error.errno)
        print(errorMsg)
        logging.critical(errorMsg)



# connect to DB
#     if connect_ok
#         upload_stored_data
#             If upload_ok
#                 Success
#             else upload_fail
#                 store data for next upload opportunity
#     else connect_fail
#         store data for next connect opportunity


