# Lineage enumeration: results

Rules: `docs/lineage_rules.md`. Code: `torus_count/hurwitz.py`, `experiments/lineage_enumeration.py`.
Weighted counts: each closed family counted once, divided by its number of symmetries (Hurwitz numbers, vortices labelled).

## 1. No vortices: closed families are counted by the divisor sum

| children d | weighted count | × d | σ(d), sum of divisors |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 3/2 | 3 | 3 |
| 3 | 4/3 | 4 | 4 |
| 4 | 7/4 | 7 | 7 |
| 5 | 6/5 | 6 | 6 |

For a prime number of children p there are exactly p + 1 closed families.

## 2. One vortex

| d | vortex cycles t children | weighted count | holes (genus) |
|---|---|---|---|
| 2 | 2 | 0 | — |
| 3 | 2 | 0 | — |
| 3 | 3 | 3 | 2 |
| 4 | 2 | 0 | — |
| 4 | 3 | 9 | 2 |
| 4 | 4 | 0 | — |
| 5 | 2 | 0 | — |
| 5 | 3 | 27 | 2 |
| 5 | 4 | 0 | — |
| 5 | 5 | 40 | 3 |

## 3. Two vortices

| d | cycles (t₁, t₂) | weighted count | holes (genus) | modular-form prediction ×2 |
|---|---|---|---|---|
| 2 | (2, 2) | 2 | 2 | 2 |
| 3 | (2, 2) | 16 | 2 | 16 |
| 3 | (2, 3) | 0 | — |  |
| 3 | (3, 3) | 9 | 3 |  |
| 4 | (2, 2) | 60 | 2 | 60 |
| 4 | (2, 3) | 0 | — |  |
| 4 | (2, 4) | 64 | 3 |  |
| 4 | (3, 3) | 135 | 3 |  |
| 4 | (3, 4) | 0 | — |  |
| 4 | (4, 4) | 80 | 4 |  |
| 5 | (2, 2) | 160 | 2 | 160 |
| 5 | (2, 3) | 0 | — |  |
| 5 | (2, 4) | 512 | 3 |  |
| 5 | (2, 5) | 0 | — |  |
| 5 | (3, 3) | 729 | 3 |  |
| 5 | (3, 4) | 0 | — |  |
| 5 | (3, 5) | 900 | 4 |  |
| 5 | (4, 4) | 1792 | 4 |  |
| 5 | (4, 5) | 0 | — |  |
| 5 | (5, 5) | 1240 | 5 |  |

## 4. Phase-wheel version (all moves are rotations)

A configuration closes exactly when the charges add to a whole number. With charges of denominator 2, 3 or 4:

| vortices | closing with total 0 | closing with any whole total | examples (total 0) |
|---|---|---|---|
| 1 | 0 | 0 | — |
| 2 | 5 | 11 | (-2/3, 2/3), (-1/3, 1/3) |
| 3 | 6 | 20 | (-2/3, 1/3, 1/3), (-1/3, -1/3, 2/3) |
