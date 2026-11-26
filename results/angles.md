# Why the golden ratio: the angle between the mother and father lines

Code: `torus_count/angles.py`. Tests: `tests/test_angles.py`.

## Theorem (families whose mother and father maps commute)

If moving to the mother-child and moving to the father-child commute, the family is a rotation
family: N tori on a cycle, mother step = shift by a, father step = shift by b. Let

    L = N / gcd(a − b, N),

the number of generations it takes the mother and father lines to come back into step. Then:

* the largest non-trivial eigenvalue is exactly **2·cos(π / L)**;
* the family obeys the graph Riemann hypothesis **exactly when L ≤ 4**.

| L | largest non-trivial eigenvalue | graph RH |
|---|---|---|
| 3 | 2 cos 60° = 1 | yes |
| 4 | 2 cos 45° = √2 | yes, on the boundary |
| **5** | **2 cos 36° = 1.618…, the golden ratio** | **no** |
| 6 | 2 cos 30° = √3 = 1.732… | no |
| 7, 8, … | 1.802…, 1.848…, rising toward 2 | no |

**Proof.** The eigenvalues are e^{2πika/N} + e^{2πikb/N}, of size 2|cos(π k (a − b)/N)|. As k
varies, k(a − b)/N runs through the multiples of 1/L. Those that are whole numbers give the
trivial eigenvalues (size 2). Of the rest, the one closest to a whole number is 1/L, giving
2 cos(π/L). This is at most √2 exactly when π/L ≥ π/4, that is L ≤ 4. ∎

Checked numerically on all 7,644 rotation families from 6 to 60 tori.

## Where the golden ratio came from

The 10-torus families that fail the graph Riemann hypothesis have L = 5: their mother and father
lines take five generations to realign, the angle of a pentagon. 2 cos 36° is the golden ratio.
The 8-torus star families have L = 4 and sit exactly on the boundary at √2.

The same numbers appear elsewhere in mathematics. 2 cos(π/L) is the largest eigenvalue of a
path of L − 1 points (the Dynkin diagram A_{L−1}), and its square 4 cos²(π/L) runs through
Jones's allowed index values 1, 2, φ² = 2.618…, 3, …. Requiring the graph Riemann hypothesis
admits only the first two.

## Families whose mother and father don't commute

The clean rule doesn't carry over. In samples up to 16 tori:

* Quick realignment (the step "mother forward, father back" repeats within 4) usually goes with
  the graph Riemann hypothesis: all but 3 of the 21 such cases.
* But many families with slow realignment obey it as well: 121 of 152 at 12 tori, 220 of 315 at
  16. Non-commuting mother and father lines mix, which keeps the eigenvalues small, much as
  random networks are known to be nearly optimal.

So the angle rule is exact for commuting families. Non-commuting families are richer, and what
decides them is open.
