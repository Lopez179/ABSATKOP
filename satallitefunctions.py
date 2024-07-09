from skyfield.api import load, wgs84
from skyfield.iokit import parse_tle_file

class TleReader:
    def __init__(self):
        self.stations_url = 'https://celestrak.org/NORAD/elements/gp.php?INTDES=1998-067&FORMAT=tle'
        self.satellite = None

        self.access_TLE()

    # This method must be called before any method, however it only needs to be called once per run sequence
    def access_TLE(self):
        max_days = 0.5
        name = 'gp.php'

        # Download again if it's been a while
        if not load.exists(name) or load.days_old(name) >= max_days:
            load.download(self.stations_url, filename=name)
            print("New TLE Downloaded")
        
        # Set self.satelite so that other methods will now work
        ts = load.timescale()
        with load.open('gp.php') as f:
            satellites = list(parse_tle_file(f, ts))
            by_name = {sat.name: sat for sat in satellites}
            self.satellite = by_name['ISS (ZARYA)']

    def print_epoch(self):
        epoch_object = self.satellite.epoch.utc_jpl()
        print(epoch_object)

    def print_overhead_times(self, t0, t1, cutoff_angle):
        bluffton = wgs84.latlon(+53.527413, -113.530055)

        t, events = self.satellite.find_events(bluffton, t0, t1, altitude_degrees=cutoff_angle)
        event_names = 'rise above ' + str(cutoff_angle) + ' °', 'culminate', 'set below ' + str(cutoff_angle) + ' °'

        for ti, event in zip(t, events):
            name = event_names[event]
            print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

    def print_sunlit_ranges(self, utc_timerange):
        eph = load('de421.bsp')

        sunlit = self.satellite.at(utc_timerange).is_sunlit(eph)

        sunlit_beginnings = []
        sunlit_endings = []

        in_sunlit_period = False
        for ti, sunlit_i in zip(utc_timerange, sunlit):
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
            sunlit_endings.append(utc_timerange[-1])
        # this edge case only exists on the end, because we assume not sunlit before the beginning of the time window

        for start, end in zip(sunlit_beginnings, sunlit_endings):
            print('{} - {}'.format(
                start.utc_strftime('%Y-%m-%d %H:%M'),
                end.utc_strftime('%Y-%m-%d %H:%M')
            ))

    def print_ecclipse_ranges(self, utc_timerange):
        eph = load('de421.bsp')

        earth, sun = eph['earth'], eph['sun']
        p = (earth + self.satellite).at(utc_timerange).observe(sun).apparent()
        eclipse = p.is_behind_earth()

        eclipse_beginnings = []
        eclipse_endings = []

        in_eclipse_period = False
        for ti, eclipse_i in zip(utc_timerange, eclipse):
            if eclipse_i:
                if not in_eclipse_period:
                    eclipse_beginnings.append(ti)
                in_eclipse_period = True
            else:
                if in_eclipse_period:
                    eclipse_endings.append(ti)
                in_eclipse_period = False

        # account for edge case where a sunlit period begins during the time window but ends after
        if len(eclipse_beginnings) > len(eclipse_endings):
            eclipse_endings.append(utc_timerange[-1])
        # this edge case only exists on the end, because we assume not sunlit before the beginning of the time window

        for start, end in zip(eclipse_beginnings, eclipse_endings):
            print('{} - {}'.format(
                start.utc_strftime('%Y-%m-%d %H:%M'),
                end.utc_strftime('%Y-%m-%d %H:%M')
            ))

def DatabaseUpload(connection,date, epoch, sunlit, ecclipse):
    pass