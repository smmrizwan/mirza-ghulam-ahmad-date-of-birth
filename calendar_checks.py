"""Calendar checks for the four candidate birth Fridays (1832, 1835, 1839, 1842).
Reproduces the Hijri, Yallop and solar-Phagan figures used in both papers.
Requires Python 3 and PyEphem (pip install ephem). Times are local mean time."""
import math, datetime as dt, ephem

PLACES = {'Delhi': (28.65, 77.23), 'Lahore': (31.55, 74.34), 'Qadian': (31.82, 75.38)}

def jdn(d):                       # Julian Day Number of a Gregorian date (noon)
    return d.toordinal() + 1721425

def weekday(d):
    return d.strftime('%A')

def tabular_hijri_jdn(y, m, d, epoch='civil'):
    """JDN of a date in the 30-year arithmetical calendar (leap years 2,5,7,10,13,
    16,18,21,24,26,29). 'civil' = Friday epoch (16 Jul 622), as in Sewell & Dikshit
    and al-Tawfiqat al-Ilhamiyya; 'astronomical' = Thursday epoch, one day earlier."""
    j = d + (59 * (m - 1) + 1) // 2 + (y - 1) * 354 + (3 + 11 * y) // 30 + 1948439
    return j - 1 if epoch == 'astronomical' else j

def tabular_day(date, y, m, epoch='civil'):
    return jdn(date) - tabular_hijri_jdn(y, m, 1, epoch) + 1

def _alt(ra, dec, o):             # altitude from geocentric RA/Dec (airless)
    H = o.sidereal_time() - ra
    return math.degrees(math.asin(math.sin(o.lat) * math.sin(dec)
                                  + math.cos(o.lat) * math.cos(dec) * math.cos(H)))

def yallop_q(date, place):
    """Yallop (1997) q at 'best time' (sunset + 4/9 of lag), geocentric ARCV.
    Zones: A > +0.216 easily visible; B > -0.014 visible in perfect conditions;
    C > -0.160 optical aid needed to find; D > -0.232 optical only; E, F not visible."""
    lat, lon = place
    o = ephem.Observer(); o.lat, o.lon = str(lat), str(lon)
    o.pressure = 0; o.horizon = '-0:34'
    # local noon of the given civil date, expressed in UT
    o.date = ephem.Date(date.strftime('%Y/%m/%d') + ' 12:00') - lon / 360.0
    s, m = ephem.Sun(), ephem.Moon()
    sset = o.next_setting(s); mset = o.next_setting(m)
    o.date = sset + (mset - sset) * 4 / 9; o.horizon = '0'
    s.compute(o); m.compute(o)
    arcv = _alt(m.g_ra, m.g_dec, o) - _alt(s.g_ra, s.g_dec, o)
    arcl = math.degrees(ephem.separation((m.g_ra, m.g_dec), (s.g_ra, s.g_dec)))
    W = math.degrees(m.radius) * 60 * (1 - math.cos(math.radians(arcl)))
    return (arcv - (11.8371 - 6.3226 * W + 0.7319 * W**2 - 0.1018 * W**3)) / 10

def sighted_month_start(date, place, threshold=-0.014):
    """First day of the lunar month containing 'date': the day after the first
    evening (from the conjunction on) whose q exceeds the threshold.
    threshold -0.014 = naked eye (zones A-B); +0.216 = only an easy crescent."""
    nm = ephem.previous_new_moon(ephem.Date(date.strftime('%Y/%m/%d')))
    e = ephem.Date(nm).datetime().date()
    while yallop_q(e, place) <= threshold:
        e += dt.timedelta(days=1)
    return e + dt.timedelta(days=1)

# Surya Siddhanta true sun (simplified: mean sun + equation of centre).
SID_YEAR, KALI = 365.258756484, 588465.5          # sidereal year; Kali epoch (JD)
def ss_true_sun(jd):
    L = (360 * (jd - KALI) / SID_YEAR) % 360
    M = math.radians(L - 77.29)                   # apogee c. 1839 (77.13 at the Kali epoch + 387 rev. per kalpa)
    p = 14 - (20 / 60) * abs(math.sin(M))
    return (L - math.degrees(math.asin(p / 360 * math.sin(M)))) % 360

def sankranti(target, before):
    """Lahore local date and time of the last entry of the sun into 'target'
    degrees on or before the date 'before'."""
    f = lambda jd: ((ss_true_sun(jd + 75.77 / 360) - target + 180) % 360) - 180
    b = ephem.julian_date(before.strftime('%Y/%m/%d')) + 1
    a = b - 1
    while f(a) > 0:               # step back a day at a time to bracket the entry
        a, b = a - 1, a
    for _ in range(60):
        mid = (a + b) / 2
        a, b = (a, mid) if f(mid) > 0 else (mid, b)
    return ephem.Date((a + b) / 2 - 2415020 + 74.34 / 360).datetime()

def solar_phagan_day(date):
    """Day of solar Phagan (sun in Aquarius, 300 deg), counted from the civil date
    of the sankranti as day 1. Before dawn, subtract one (day runs from sunrise)."""
    start = sankranti(300, date).date()
    return (date - start).days + 1

CANDIDATES = [  # (Friday, Hijri year, Hijri month)
    (dt.date(1832, 2, 17), 1247, 9), (dt.date(1835, 2, 13), 1250, 10),
    (dt.date(1839, 3, 1), 1254, 12), (dt.date(1842, 2, 25), 1258, 1)]

if __name__ == '__main__':
    print('Friday      civil astro Delhi Lahore Qadian easy-only Phagan(by day)')
    for f, y, m in CANDIDATES:
        assert weekday(f) == 'Friday'
        row = [tabular_day(f, y, m), tabular_day(f, y, m, 'astronomical')]
        for p in ('Delhi', 'Lahore', 'Qadian'):
            row.append((f - sighted_month_start(f, PLACES[p])).days + 1)
        row.append((f - sighted_month_start(f, PLACES['Qadian'], 0.216)).days + 1)
        row.append(solar_phagan_day(f))
        print(f, '   '.join(str(x).rjust(2) for x in row))
    entry = sankranti(300, dt.date(1839, 3, 1))
    print('Aquarius entry 1839:', entry.strftime('%Y-%m-%d %H:%M'))
    for e in [(1835, 1, 29), (1835, 1, 30), (1839, 2, 14), (1839, 2, 15),
              (1842, 2, 11), (1842, 2, 12)]:
        d = dt.date(*e)
        print('q', d, ' '.join(f'{p} {yallop_q(d, c):+.2f}' for p, c in PLACES.items()))
