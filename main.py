from skyfield.api import load, wgs84
from satallitefunctions import *
import sqlite3
import datetime

today = datetime.datetime.now()

connection = sqlite3.connect('mainDatabase.db')
mainCursor = connection.cursor()

MainTleReader = TleReader()

# Get the epoch
epoch_obj = MainTleReader.print_epoch()
print(epoch_obj)
print(" ")

# Get overhead times --------------------------------------------------------------------------------

ts = load.timescale()
t0 = ts.utc(today.year, today.month, today.day)
t1 = ts.utc(today.year, today.month, today.day + 5)

overheadtimes = MainTleReader.print_overhead_times(t0, t1, 63)
for i in overheadtimes:
    print(i)
print(" ")

# Get sunlit times -----------------------------------------------------------------------------------
utc_timerange = ts.utc(today.year, today.month, today.day, today.hour, range(0, 6 * 60, 1))

sunlittimes = MainTleReader.print_sunlit_ranges(utc_timerange)
for i in sunlittimes:
    print(i)
print(" ")

# Get in ecclipse time -------------------------------------------------------------------------------
ecclipsetimes = MainTleReader.print_ecclipse_ranges(utc_timerange)
for i in ecclipsetimes:
    print(i)

# Load into database ---------------------------------------------------------------------------------


mainCursor.execute("INSERT INTO TimeRecord (date, epoch, overhead, timerange_sunlit) VALUES (?, ?, ?,?)", (str(today), str(epoch_obj), str(overheadtimes), str(sunlittimes)))
connection.commit()
connection.close()