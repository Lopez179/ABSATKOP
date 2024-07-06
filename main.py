from skyfield.api import load, wgs84
from satallitefunctions import *

# Get the satalite ISS TLE from the internet
stations_url = 'https://celestrak.org/NORAD/elements/gp.php?INTDES=1998-067&FORMAT=tle'
satellites = load.tle_file(stations_url, reload=True)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']

# Get the epoch
epoch_object = satellite.epoch.utc_jpl()
print(" ")
print(epoch_object)

# Get overhead times --------------------------------------------------------------------------------
ts = load.timescale()
bluffton = wgs84.latlon(+53.527413, -113.530055)
t0 = ts.utc(2024, 6, 25)
t1 = ts.utc(2024, 7, 30)

cutoff_angle = 65

t, events = satellite.find_events(bluffton, t0, t1, altitude_degrees=cutoff_angle)
event_names = 'rise above ' + str(cutoff_angle) + ' °', 'culminate', 'set below ' + str(cutoff_angle) + ' °'
print(" ")
for ti, event in zip(t, events):
    name = event_names[event]
    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

# Get sunlit times -----------------------------------------------------------------------------------
eph = load('de421.bsp')

twentyfour_hours = ts.utc(2024, 7, 5, 0, range(0, 24 * 60, 1))
sunlit = satellite.at(twentyfour_hours).is_sunlit(eph)

sunlit_beginnings = []
sunlit_endings = []

in_sunlit_period = False
for ti, sunlit_i in zip(twentyfour_hours, sunlit):
    if sunlit_i:
        if not in_sunlit_period:
            sunlit_beginnings.append(ti)
        in_sunlit_period = True
    else:
        if in_sunlit_period:
            sunlit_endings.append(ti)
        in_sunlit_period = False

# account for edge case where a sunlit period begins during the time window but ends after
if len(sunlit_beginnings) > len(sunlit_endings):
    sunlit_endings.append(twentyfour_hours[-1])
# this edge case only exists on the end, because we assume not sunlit before the beginning of the time window

for start, end in zip(sunlit_beginnings, sunlit_endings):
    print('{} - {}'.format(
        start.utc_strftime('%Y-%m-%d %H:%M'),
        end.utc_strftime('%Y-%m-%d %H:%M')
    ))


# Get in ecclipse time -------------------------------------------------------------------------------
#eph = load('de421.bsp')
#earth, sun = eph['earth'], eph['sun']

#twentyfour_hours = ts.utc(2024, 6, 25, 0, range(0, 24 * 60, 20))
#p = (earth + satellite).at(twentyfour_hours).observe(sun).apparent()
#sunlit = p.is_behind_earth()
#print(sunlit)

