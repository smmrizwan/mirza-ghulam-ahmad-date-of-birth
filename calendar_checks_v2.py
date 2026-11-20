"""Calendar checks, version 2 (28 Oct 2026).
Adds to calendar_checks.py: a month-by-month Hijri count that applies the
29/30-day rule (a month ends after 29 days if the crescent is visible on the
29th evening, otherwise after 30), every Friday in solar Phagan 1830-1844,
and a one-day-late column (the deciding crescent missed, e.g. through cloud).
Requires Python 3, PyEphem (pip install ephem) and calendar_checks.py in the
same folder. Times are local mean time, place Lahore unless stated."""
import datetime as dt, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendar_checks as cc

MONTHS = ['Muharram', 'Safar', "Rabi' I", "Rabi' II", 'Jumada I', 'Jumada II',
          'Rajab', "Sha'ban", 'Ramadan', 'Shawwal', "Dhu al-Qa'da", 'Dhu al-Hijja']

def month_table(place, start_y=1245, end_y=1261, threshold=-0.014):
    """Propagate months from the sighted start of Muharram start_y.
    Returns a list of (hijri year, month index 1-12, first day, length,
    q on the 29th evening)."""
    jd = cc.tabular_hijri_jdn(start_y, 1, 1)
    first = dt.date.fromordinal(jd - 1721425)
    first = cc.sighted_month_start(first + dt.timedelta(days=5), place, threshold)
    out, y, m = [], start_y, 1
    while y < end_y:
        eve29 = first + dt.timedelta(days=28)          # evening ending day 29
        q = cc.yallop_q(eve29, place)
        length = 29 if q > threshold else 30
        out.append((y, m, first, length, q))
        first = first + dt.timedelta(days=length)
        m += 1
        if m == 13: y, m = y + 1, 1
    return out

def hijri_of(date, table):
    """(year, month, day, length of the previous month) for a date."""
    for i, (y, m, first, length, q) in enumerate(table):
        if first <= date < first + dt.timedelta(days=length):
            return y, m, (date - first).days + 1, table[i - 1][3]
    return None

def tabular_hijri(date, epoch='civil'):
    """(year, month, day) of a date in the arithmetical calendar."""
    j = cc.jdn(date)
    y = (30 * (j - 1948440) + 10646) // 10631
    while cc.tabular_hijri_jdn(y, 1, 1, epoch) > j: y -= 1
    while cc.tabular_hijri_jdn(y + 1, 1, 1, epoch) <= j: y += 1
    m = 1
    while m < 12 and cc.tabular_hijri_jdn(y, m + 1, 1, epoch) <= j: m += 1
    return y, m, j - cc.tabular_hijri_jdn(y, m, 1, epoch) + 1

def phagan_fridays(y0=1830, y1=1844):
    for y in range(y0, y1 + 1):
        start = cc.sankranti(300, dt.date(y, 2, 20)).date()
        end = cc.sankranti(330, dt.date(y, 3, 20)).date()
        d = start
        while d.weekday() != 4: d += dt.timedelta(days=1)
        while d < end:
            yield d, (d - start).days + 1
            d += dt.timedelta(days=7)

if __name__ == '__main__':
    place = cc.PLACES['Lahore']
    table = month_table(place)
    if '--months' in sys.argv:
        print('Hijri month          first day   len  q on 29th evening')
        for y, m, first, length, q in table:
            print(f'{MONTHS[m-1]:<13} {y}  {first}  {length}  {q:+.2f}')
    print('Friday     Ph  Hijri by sighting (29/30 rule)  one day late    civil tables')
    for d, ph in phagan_fridays():
        h = hijri_of(d, table)
        if not h: continue
        y, m, day, prev = h
        ty, tm, td = tabular_hijri(d)
        civ = str(td) if (ty, tm) == (y, m) else f'{td} {MONTHS[tm-1]}'
        # A month can start a day late only if the previous month had ended
        # after 29 days on a sighting; after 30 days the next day is forced.
        late = str(day - 1) if prev == 29 else '- (30-day rule)'
        flag = ' MATCH' if day == 14 else (' (14th if the deciding crescent was missed)' if prev == 29 and day == 15 else '')
        print(f'{d}  {ph:>2}  {day:>2} {MONTHS[m-1]:<13} {y}  {late:<15} {civ:>2}{flag}')
