from skyfield.api import load, wgs84
from satallitefunctions import *
import sqlite3
import datetime

today = datetime.datetime.now()

connection = sqlite3.connect('mainDatabase.db')
mainCursor = connection.cursor()

MainTleReader = TleReader()

# Get the epoch
MainTleReader.print_epoch()
print(" ")

# Get overhead times --------------------------------------------------------------------------------

ts = load.timescale()
t0 = ts.utc(today.year, today.month, today.day)
t1 = ts.utc(today.year, today.month, today.day + 5)
MainTleReader.print_overhead_times(t0, t1, 63)
print(" ")

# Get sunlit times -----------------------------------------------------------------------------------
utc_timerange = ts.utc(today.year, today.month, today.day, today.hour, range(0, 6 * 60, 1))

MainTleReader.print_sunlit_ranges(utc_timerange)
print(" ")

# Get in ecclipse time -------------------------------------------------------------------------------
MainTleReader.print_ecclipse_ranges(utc_timerange)


