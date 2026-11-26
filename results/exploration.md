# What the draft-4 rules allow

Rules: `docs/lineage_rules.md`, draft 4. Code: `torus_count/explore.py`.

## Families

| tori | distinct families (exhaustive) |
|---|---|
| 8 | 2 (both star tetrahedra) |
| 10 | 5 |

Larger sizes were sampled at random (12, 14, 16, 20 tori).

## Generational loops and the fractions they allow

| tori | loops by length (simple loops) | denominators that balancing can produce |
|---|---|---|
| 8 | 4: 12, 6: 16, 8: 2 | 1, 2, 3, 4 |
| 10 (two families) | 4: 10, 6: 20, 8: 20, 10: 4 | 1, 2, 3, 4, 5 |
| 10 (three families) | 4: 10, 6: 25, 8: 10, 10: 4 | 1, 2, 3, 4, 5 |

Charge put on one loop is balanced by loops of other lengths, so the allowed fractions are set
by ratios of loop lengths. For example +1 on a 4-loop is balanced by −2/3 on a 6-loop. Loops are
always of even length, because generations alternate between the two dual sets. A family on 2m
tori has as many independent balanced charge patterns as it has tori.

## Prime loops

A primitive loop is a generational loop that isn't a shorter loop repeated. These are graph
theory's analogue of primes, and their counts come from traces of the family's connection matrix.

| tori | primitive loops of length 4, 6, 8, 10 |
|---|---|
| 8 | 12, 16, 66, 192 |
| 10 (two families) | 10, 20, 60, 204 |
| 10 (three families) | 10, 25, 40, 254 |

## The graph Riemann hypothesis

A family's zeta function, 1 / det(I − uA), is built from its primitive loops just as the Riemann
zeta function is built from primes. The graph version of the Riemann hypothesis (the
"Ramanujan" condition) asks that every eigenvalue of A other than the trivial ±2 has size at
most √2.

| tori | families satisfying it | largest non-trivial eigenvalue |
|---|---|---|
| 8 | 2 of 2 | exactly √2 = 1.414 (on the boundary) |
| 10 | 2 of 5 | 1.0 in the two that satisfy it; **the golden ratio 1.618** in the three that fail |
| 12 | 82% of 231 sampled | median √2, maximum 1.732 |
| 14 | 57% of 284 sampled | median √2, maximum 1.732 |
| 16 | 65% of 300 sampled | median √2, maximum 1.784 |
| 20 | 52% of 300 sampled | median √2, maximum 1.772 |

The three 10-torus families that fail have eigenvalues of exactly 2, the golden ratio φ and
1/φ.

## Caveats

* The graph Riemann hypothesis is a well-studied analogue (Ihara zeta functions and Ramanujan
  graphs), not the Riemann hypothesis itself.
* Random samples are of labelled families, so they're not uniform over distinct families.
