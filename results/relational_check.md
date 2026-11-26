# Time as the relations of change: the rewrite and its test

The simulation was rewritten with no external time. The only parameter is the
system's own poloidal phase; every rate is one change per another change.

Run: `python3 -m experiments.relational_check` (numbers in `relational_check.json`).
Tests: `python3 -m pytest -q` (98 pass).

## Results (135 cells: 9 values of ε × 5 of δ × 3 winding ratios, 40 toroidal turns)

| Check | Result |
|---|---|
| Clock-free rewrite vs the original simulation | identical in 135/135 cells |
| Uneven outside clock driving **everything**, shutter included (rate swinging 10%–190%) | identical in 135/135 cells, at every unevenness tested |
| Uneven outside clock driving **only the shutter** | counts change in 13% / 25% / 36% of cells (unevenness 0.3 / 0.6 / 0.9); mean error vs truth 0.13 / 0.28 / 0.39 (original 0.15) |
| Truth, portal-pass decisions, coherence runs | never refer to any clock, so they are unaffected by construction |
| Known results (three-gap, continued fractions, Fibonacci returns, Kac, Nyquist, ε = 0 divisor rule) | all pass in the clock-free form |

## Which changes can serve as a clock

A clock has to be a change that never reverses.

| Setting | Toroidal phase usable as a clock |
|---|---|
| no locking | yes, at every ε |
| locking on | only at ε = 0, where the pull vanishes; elsewhere the pull steps it backward at passes |
| mirror flip (ε < 0) | no; the mirror reverses it |

The poloidal phase is always a valid clock in this model, because the gate and
the pull act only on the toroidal phase.

## Reading

* The old external time was the poloidal phase divided by ω all along.
* Re-timing every change together changes nothing, so no result depends on an
  absolute time. Part of this holds by construction once everything is written
  relationally; the numerical run confirms nothing escaped that cancellation.
* The only place a clock entered was the observer's shutter. Its counts depend
  on the relation between the shutter's change and the system's change, which
  is a relation of changes, not absolute time.
