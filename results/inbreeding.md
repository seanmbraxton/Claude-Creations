# What decides the graph Riemann hypothesis for a family

Code: `torus_count/groups.py`, `torus_count/angles.py`. Builds on `results/angles.md`.

## 1. It is decided by the grandchild network (exact)

Generations alternate between the two dual sets, so a family's eigenvalues are the square roots
of the eigenvalues of its **grandchild network**: the network on one dual set in which every
torus points to its four grandchildren (mother's mother-child, mother's father-child,
father's mother-child, father's father-child). Checked on every 8- and 10-torus family with
zero error.

So a family obeys the graph Riemann hypothesis exactly when its grandchild network does, with
the bound √4 = 2.

## 2. Commuting families: decided by an angle (proved)

When the mother and father moves commute, the largest non-trivial eigenvalue is 2 cos(π/L), and
the condition holds exactly when the two lines realign within L ≤ 4 generations. The golden
ratio is L = 5. See `results/angles.md`.

## 3. Everyone else: inbreeding pushes a family past the bound (statistical)

A **repeated grandchild** is a torus reached by two different routes, for example when a torus's
mother's father-child is the same as its father's mother-child. Two lineages reconverge.

Random families, 10 to 22 tori (about 1,000):

| repeated grandchildren per torus | obey | typical worst eigenvalue |
|---|---|---|
| none | 87% | 1.375 |
| up to 0.3 | 73% | 1.399 |
| 0.3–0.6 | 66% | 1.414 |
| 0.6–1 | 48% | 1.423 |
| every torus | **7%** | **1.618 (golden ratio)** |

Lineages that stay distinct one more generation (first reconverging at the great-grandchildren)
obeyed it 96% of the time, against 60%.

The effect fades in larger families:

| tori | least reconvergence → most | correlation with worst eigenvalue |
|---|---|---|
| 32 | 66% → 42% → 31% | 0.42 |
| 48 | 50% → 43% → 35% | 0.06 |

## 4. A size limit on distinct lineages

Keeping r generations of lineage distinct takes 2^r different descendants in one dual set, so it
needs at least 2·2^r tori. Small families have to inbreed early. Random large families almost
always reconverge at the grandchildren anyway: the same birthday-paradox effect that makes
coincidences common.

## Reading

Families that obey the graph Riemann hypothesis behave as closely as a finite family can like
an ideal, inbreeding-free family tree. That matches what's known in graph theory: the √(degree)
bound is the spectral signature of the infinite tree, and Ramanujan networks are the finite
networks that imitate it best. Reconverging lineages are where a finite family visibly falls
short of the tree, and a family in which every torus has a reconverging grandchild is pushed
furthest, typically to the golden ratio.

## Open

* In large families, what decides the outcome beyond grandchild reconvergence. Large random
  networks are known to hover right at the bound, so small fluctuations may dominate.
* Whether a rule forbidding repeated grandchildren (no inbreeding at the second generation)
  ever guarantees the condition. In the samples it raises the odds but doesn't guarantee them.
