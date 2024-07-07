from skyfield.api import load, wgs84
from satallitefunctions import *

# Get the epoch
print_epoch()

# Get overhead times --------------------------------------------------------------------------------

ts = load.timescale()
t0 = ts.utc(2024, 6, 25)
t1 = ts.utc(2024, 7, 30)
print_overhead_times(t0, t1, 63.9)

# Get sunlit times -----------------------------------------------------------------------------------
utc_timerange = ts.utc(2024, 7, 5, 0, range(0, 24 * 60, 1))
#print_sunlit_ranges(utc_timerange)

# Get in ecclipse time -------------------------------------------------------------------------------
print_ecclipse_ranges(utc_timerange)

