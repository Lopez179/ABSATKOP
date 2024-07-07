from skyfield.api import load, wgs84

stations_url = 'https://celestrak.org/NORAD/elements/gp.php?INTDES=1998-067&FORMAT=tle'

def print_epoch():
    satellites = load.tle_file(stations_url, reload=True)
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['ISS (ZARYA)']

    epoch_object = satellite.epoch.utc_jpl()
    print(epoch_object)

def print_overhead_times(t0, t1, cutoff_angle):
    satellites = load.tle_file(stations_url, reload=True)
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['ISS (ZARYA)']

    bluffton = wgs84.latlon(+53.527413, -113.530055)

    t, events = satellite.find_events(bluffton, t0, t1, altitude_degrees=cutoff_angle)
    event_names = 'rise above ' + str(cutoff_angle) + ' °', 'culminate', 'set below ' + str(cutoff_angle) + ' °'
    print(" ")
    for ti, event in zip(t, events):
        name = event_names[event]
        print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

def print_sunlit_ranges(utc_timerange):
    satellites = load.tle_file(stations_url, reload=True)
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['ISS (ZARYA)']

    ts = load.timescale()
    eph = load('de421.bsp')

    sunlit = satellite.at(utc_timerange).is_sunlit(eph)

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

def print_ecclipse_ranges(utc_timerange):
    satellites = load.tle_file(stations_url, reload=True)
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['ISS (ZARYA)']

    eph = load('de421.bsp')

    earth, sun = eph['earth'], eph['sun']
    p = (earth + satellite).at(utc_timerange).observe(sun).apparent()
    eclipse = p.is_behind_earth()

    eclipse_beginnings = []
    eclipse_endings = []

    in_eclipse_period = False
    for ti, eclipse_i in zip(utc_timerange, eclipse):
        if eclipse_i:
            if not in_sunlit_period:
                eclipse_beginnings.append(ti)
            in_sunlit_period = True
        else:
            if in_sunlit_period:
                eclipse_endings.append(ti)
            in_sunlit_period = False

    # account for edge case where a sunlit period begins during the time window but ends after
    if len(eclipse_beginnings) > len(eclipse_endings):
        eclipse_endings.append(utc_timerange[-1])
    # this edge case only exists on the end, because we assume not sunlit before the beginning of the time window

    for start, end in zip(eclipse_beginnings, eclipse_endings):
        print('{} - {}'.format(
            start.utc_strftime('%Y-%m-%d %H:%M'),
            end.utc_strftime('%Y-%m-%d %H:%M')
        ))