from skyfield.api import load, wgs84
from satallitefunctions import *

MainTleReader = TleReader()

# Get the epoch
MainTleReader.print_epoch()
print(" ")

# Get overhead times --------------------------------------------------------------------------------

ts = load.timescale()
t0 = ts.utc(2024, 7, 1)
t1 = ts.utc(2024, 7, 30)
MainTleReader.print_overhead_times(t0, t1, 63)
print(" ")

# Get sunlit times -----------------------------------------------------------------------------------
utc_timerange = ts.utc(2024, 7, 7, 0, range(0, 24 * 60, 1))
MainTleReader.print_sunlit_ranges(utc_timerange)
print(" ")

# Get in ecclipse time -------------------------------------------------------------------------------
MainTleReader.print_ecclipse_ranges(utc_timerange)

