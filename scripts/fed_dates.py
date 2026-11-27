"""Shared federal calendar helpers: OPM holiday rules, leave years, NFC pay dates."""
import datetime as dt

D, T = dt.date, dt.timedelta


def nth_weekday(y, m, wd, n):
    d = D(y, m, 1)
    d += T((wd - d.weekday()) % 7)
    return d + T(7 * (n - 1))


def last_weekday(y, m, wd):
    d = D(y, m + 1, 1) - T(1) if m < 12 else D(y, 12, 31)
    return d - T((d.weekday() - wd) % 7)


def observed(d):
    return d - T(1) if d.weekday() == 5 else d + T(1) if d.weekday() == 6 else d


def holidays(y):
    """Federal holidays observed in calendar year y (5 U.S.C. 6103), as {date: name}."""
    h = {
        observed(D(y, 1, 1)): "New Year's Day",
        nth_weekday(y, 1, 0, 3): 'Martin Luther King Jr. Day',
        nth_weekday(y, 2, 0, 3): "Washington's Birthday",
        last_weekday(y, 5, 0): 'Memorial Day',
        observed(D(y, 6, 19)): 'Juneteenth',
        observed(D(y, 7, 4)): 'Independence Day',
        nth_weekday(y, 9, 0, 1): 'Labor Day',
        nth_weekday(y, 10, 0, 2): 'Columbus Day',
        observed(D(y, 11, 11)): 'Veterans Day',
        nth_weekday(y, 11, 3, 4): 'Thanksgiving Day',
        observed(D(y, 12, 25)): 'Christmas Day',
    }
    nxt = observed(D(y + 1, 1, 1))
    if nxt.year == y:          # New Year's Day of y+1 observed on Dec 31 of y
        h[nxt] = "New Year's Day (observed)"
    return {d: n for d, n in h.items() if d.year == y}


HOL = {}
for _y in range(2025, 2031):
    HOL.update(holidays(_y))


def leave_year_start(y):
    """OPM: leave year begins the first day of the first full biweekly pay period in the calendar year.
    Federal biweekly periods are anchored to Sunday, January 10, 2027."""
    anchor = D(2027, 1, 10)
    d = D(y, 1, 1)
    off = (d - anchor).days % 14
    return d if off == 0 else d + T(14 - off)


def nfc(end):
    """NFC deposit: second Monday after the period ends (Tuesday if that Monday is a holiday); official pay date is that Thursday."""
    mon = end + T(9)
    return (mon + T(1) if mon in HOL else mon), end + T(12)


def periods(y):
    s0, s1 = leave_year_start(y), leave_year_start(y + 1)
    out, s, n = [], s0, 1
    while s < s1:
        e = s + T(13)
        dep, off = nfc(e)
        out.append((n, s, e, dep, off))
        s += T(14); n += 1
    return out


# Self-checks against the published 2027 schedule and OPM leave years
assert leave_year_start(2026) == D(2026, 1, 11) and leave_year_start(2027) == D(2027, 1, 10) and leave_year_start(2028) == D(2028, 1, 9)
assert len(periods(2026)) == 26 and len(periods(2027)) == 26
p27 = periods(2027)
assert p27[0][3:] == (D(2027, 2, 1), D(2027, 2, 4)) and p27[1][3] == D(2027, 2, 16) and p27[11][3] == D(2027, 7, 6)
assert p27[18][3] == D(2027, 10, 12) and p27[25][3] == D(2028, 1, 18)
p26 = periods(2026)
assert p26[24][3] == D(2027, 1, 4) and p26[25][3] == D(2027, 1, 19)
assert HOL[D(2027, 12, 31)] == "New Year's Day (observed)" and HOL[D(2027, 6, 18)] == 'Juneteenth' and HOL[D(2026, 7, 3)] == 'Independence Day'
