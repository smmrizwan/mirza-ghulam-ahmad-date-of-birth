# Calendar code for "The Date of Birth of Mirza Ghulam Ahmad in the Light of the Evidence"

This repository holds the calendar scripts and their outputs for the working paper
*The Date of Birth of Mirza Ghulam Ahmad in the Light of the Evidence* by
Dr. Sheikh Muhammad Rizwan. The paper will be published at
<https://archive.org/details/mirza-ghulam-ahmad-date-of-birth>.

The three main scripts are printed in full in Appendix C of the paper. The files here
are the same code, so that anyone can run it and check every calendar figure in the
paper.

## What is here

- `calendar_checks.py` (Appendix C.1): weekday by Julian Day Number, the arithmetical
  Hijri tables (civil and astronomical epochs), Yallop's q for crescent visibility
  (geocentric ARCV), month starts by sighting, and the Surya Siddhanta true sun for
  the Bikrami solar month (Phagan = the sun entering Kumbha).
- `calendar_checks_v2.py` (Appendix C.3): carries the Hijri months forward from
  Muharram 1245 with the 29/30-day rule (a month ends after 29 days if the crescent
  is visible on the 29th evening, otherwise after 30). It lists every Friday in solar
  Phagan from 1830 to 1844 with its Hijri day and a one-day-late column.
  `--months` also prints the month table.
- `miss_sim.py` (Appendix C.3, not printed in the paper): how many missed crescents
  (evenings clouded out) it takes to move each Phagan Friday on or off the 14th.
- `friday14.py` (Appendix C.4): every Friday from 1830 to 1844 on the 14th of a Hijri
  month, by sighting (26) and by the tables (25), with those in solar Phagan marked
  (Table 15 of the paper).
- `outputs/`: the output of each script, exactly as printed in the paper.

| Output file | Command |
|---|---|
| `outputs/calendar_checks_output.txt` | `python calendar_checks.py` |
| `outputs/calendar_checks_v2_fridays.txt` | `python calendar_checks_v2.py` |
| `outputs/calendar_checks_v2_months_and_fridays.txt` | `python calendar_checks_v2.py --months` (the month table) |
| `outputs/miss_sim_output.txt` | `python miss_sim.py` |
| `outputs/friday14_output.txt` | `python friday14.py` |

## How to run

Python 3 (tested on 3.13) and PyEphem 4.2.1:

    pip install -r requirements.txt
    python calendar_checks.py
    python calendar_checks_v2.py --months
    python miss_sim.py
    python friday14.py

Each script runs in a few seconds. Keep all four files in the same folder, because
the later scripts import `calendar_checks.py` and `calendar_checks_v2.py`.

Place: Lahore (31.55° N, 74.34° E) unless stated. Times are local mean time.
Visibility threshold: the Yallop zone B/C boundary, q = −0.014.

## Limits

Crescent visibility is a model, not an observation. A q near the threshold
(16 January 1839, q −0.01) could go either way, though with the 30-day rule that
crescent alone does not move 1 March 1839. The 1839 result therefore depends on a
sighting count at Qadian, which is not recorded. See the paper, Parts 4 and 5.6.

## Corrections

Please send corrections to mrizwan@yahoo.com.

## Licence

The code and outputs are released under the MIT Licence (see `LICENSE`).
The paper itself is released separately under CC BY 4.0.
