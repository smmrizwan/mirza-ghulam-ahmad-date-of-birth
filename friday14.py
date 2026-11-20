"""Every Friday that fell on the 14th of a Hijri month, 1 Jan 1830 - 31 Dec 1844,
without the Phagan condition. Sighting model: the month table of
calendar_checks_v2.py (Lahore, Yallop q > -0.014 on the 29th evening).
Tabular model: the civil-epoch arithmetic calendar of calendar_checks.py.
Requires Python 3, PyEphem and both calendar_checks files in the same folder."""
import datetime as dt, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendar_checks as cc
import calendar_checks_v2 as v2

def tabular_of(d):
    """(year, month, day) of a date in the civil-epoch tabular calendar."""
    j = cc.jdn(d)
    for y in range(1244, 1262):
        for m in range(1, 13):
            if cc.tabular_hijri_jdn(y, m, 1) <= j < (cc.tabular_hijri_jdn(y, m + 1, 1) if m < 12 else cc.tabular_hijri_jdn(y + 1, 1, 1)):
                return y, m, j - cc.tabular_hijri_jdn(y, m, 1) + 1

def in_phagan(d):
    s = cc.sankranti(300, dt.date(d.year, 2, 20)).date()
    e = cc.sankranti(330, dt.date(d.year, 3, 20)).date()
    return s <= d < e

if __name__ == '__main__':
    table = v2.month_table(cc.PLACES['Lahore'])
    d = dt.date(1830, 1, 1)
    while d.weekday() != 4: d += dt.timedelta(days=1)
    sight, tab = [], []
    while d <= dt.date(1844, 12, 31):
        h = v2.hijri_of(d, table)
        if h and h[2] == 14: sight.append((d, h[0], h[1]))
        t = tabular_of(d)
        if t[2] == 14: tab.append((d, t[0], t[1]))
        d += dt.timedelta(days=7)
    print('Friday on the 14th, by sighting (Lahore)')
    for d, y, m in sight:
        print(f'{d}  14 {v2.MONTHS[m-1]:<13} {y}' + ('  PHAGAN' if in_phagan(d) else ''))
    common = set(x[0] for x in sight) & set(x[0] for x in tab)
    print(f'by sighting: {len(sight)}; by the tables: {len(tab)}; in common: {len(common)}')
    print('Friday on the 14th, tables only:', ', '.join(str(x[0]) for x in tab if x[0] not in common))
    print('Friday on the 14th, sighting only:', ', '.join(str(x[0]) for x in sight if x[0] not in common))
