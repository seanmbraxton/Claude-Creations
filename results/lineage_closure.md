# Closed lineages under the grandparent rule

Rules: `docs/lineage_rules.md` (draft 2). Code: `torus_count/lineage.py`. Tests: `tests/test_lineage.py`.

## Theorem: every family is a three-generation loop

Under the rules (charges sum to zero on each torus, so at least two children; every child
spawns its grandparent; nobody is its own child), the tori split into three generations
A, B, C, and

* every torus in A spawns every torus in B,
* every torus in B spawns every torus in C,
* every torus in C spawns every torus in A.

Nothing else is possible.

**Proof.** Take any spawn G → P.
* If P → X, the rule gives X → G. So P's children are among G's parents.
* If Y → G, then Y → G → P gives P → Y. So G's parents are among P's children.
* Hence for every spawn G → P: **children(P) = parents(G).**

Now take a triangle u → v → x → u (every spawn lies in one, because P has a child). Let
C0 = parents(v), C1 = children(u), C2 = children(v). For any u′ in C0, the spawn u′ → v gives
parents(u′) = children(v) = C2. Since x is in C2, x → u′, which gives children(u′) =
parents(x) = C1. The same argument works for C1 and C2. No torus lies in two classes, because a
spawn inside one class would close a loop of length 2 and force a torus to be its own child.
Connectedness puts every torus in one of the classes. ∎

Because every torus needs at least two children, each generation has at least two tori, so
the **smallest family has 6 tori (2 + 2 + 2)**. Every torus is its own great-grandchild:
three spawns bring you back to your own generation, and the connections are complete.

## Exhaustive search agrees

| tori | labelled families found | generation sizes | exceptions |
|---|---|---|---|
| 2–5 | 0 | — | 0 |
| 6 | 30 | (2, 2, 2) | 0 |
| 7 | 210 | (2, 2, 3) | 0 |
| 8 | 980 predicted by the theorem | (2, 2, 4), (2, 3, 3) | (run in progress) |

## How many distinct families

One per way of arranging three generation sizes (each at least 2) around the loop, up to
rotation:

| tori | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|
| families | 1 | 1 | 2 | 4 | 5 | 7 | 10 |

## Charges

A torus in a generation spawns every torus in the next, so it has as many vortices as the next
generation has tori, and their charges sum to zero.

| from a generation of a to one of b | ±1 only | thirds (±1/3, ±2/3) | ±1 and thirds |
|---|---|---|---|
| a = 2, b = 2 | 2 (4) | 4 (16) | 6 (36) |
| a = 2, b = 3 | 0 (0) | 6 (36) | 18 (324) |
| a = 3, b = 2 | 0 (8) | 6 (64) | 18 (216) |
| a = 3, b = 3 | 0 (0) | 12 (216) | 72 (5832) |

Numbers outside brackets also require arrivals to balance (charges arriving at each torus sum
to zero). Numbers in brackets only require departures to balance.

* **With only +1 and −1, every generation must have an even number of tori.** A torus with an
  odd number of children can't balance unit charges.
* **A generation of three needs unequal charges**, for example (+2, −1, −1), or the same
  pattern in thirds, (+2/3, −1/3, −1/3).
* **With every torus carrying (+2/3, −1/3, −1/3) and arrivals balanced, each child receives
  exactly one +2/3 and two −1/3.** The charge pattern passes unchanged from generation to
  generation, in 6 ways per pair of generations (the +2/3 tubes form a one-to-one matching).

## The great-grandparent rule, for comparison

If X must spawn its great-grandparent instead, the search (up to 6 tori) finds four-generation
loops, plus degenerate two-generation families where a torus and its child spawn each other.
The grandparent rule forbids the latter, because a torus would have to be its own child.
