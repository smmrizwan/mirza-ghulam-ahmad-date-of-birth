"""How many missed crescents (evenings clouded out) it takes to move each\nPhagan Friday 1830-1844 on or off the 14th, months carried with the 29/30-day rule.\nCandidate misses: the first evening the crescent was visible after conjunction,\nand the evening after. Searches one and two misses."""
import datetime as dt, itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calendar_checks as cc, calendar_checks_v2 as v2
L = cc.PLACES['Lahore']; TH = -0.014
qcache = {}
def q(d):
    if d not in qcache: qcache[d] = cc.yallop_q(d, L)
    return qcache[d]
def propagate(start, n, missed=frozenset()):
    """month starts from 'start' for n months; an evening in 'missed' is clouded out"""
    starts=[start]; s=start
    for _ in range(n):
        e = s + dt.timedelta(days=28)
        s = s + dt.timedelta(days=29 if (q(e) > TH and e not in missed) else 30)
        starts.append(s)
    return starts
base = v2.month_table(L)
def day_in(date, starts):
    for a,b in zip(starts, starts[1:]):
        if a <= date < b: return (date-a).days+1
for f, ph in v2.phagan_fridays():
    # anchor 6 months back, using baseline start there
    idx = [i for i,(y,m,first,l,qq) in enumerate(base) if first <= f < first+dt.timedelta(days=l)]
    if not idx: continue
    i = idx[0]; a = max(i-6,0); start = base[a][2]; n = i-a+2
    b = propagate(start, n); d0 = day_in(f, b)
    if d0 not in (13,14,15,16,17): continue
    # visible 29th evenings in the chain
    vis=[]; e=start
    while e < f:
        if q(e) > TH and q(e-dt.timedelta(days=1)) <= TH: vis += [e, e+dt.timedelta(days=1)]
        e += dt.timedelta(days=1)
    found=None
    for r in (1,2):
        hits=[]
        for combo in itertools.combinations(vis, r):
            d = day_in(f, propagate(start, n, frozenset(combo)))
            if (d0==14 and d!=14) or (d0!=14 and d==14): hits.append((combo, d))
        if hits: found=(r, hits); break
    if not found:
        print(f, 'baseline', d0, '-> unchanged with up to two missed crescents'); continue
    r, hits = found
    print(f, 'baseline', d0, '->', hits[0][1], 'needs', r, 'missed crescent(s);', len(hits), 'combination(s):')
    for combo, d in hits:
        print('    ', ' + '.join(f'{c} (q {q(c):+.2f})' for c in combo), '->', d)
