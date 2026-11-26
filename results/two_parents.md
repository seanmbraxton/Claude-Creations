# Two parents: the dual-tetrahedron families

Code: `torus_count/two_parents.py`. Tests: `tests/test_two_parents.py`.

## The rules tested

* Every torus has **two parents**, one at each input of its axis: one sends a +1 tube into one
  end and the other sends a −1 tube into the other end.
* Every torus's vortex charges net zero, and it has a +1 child and a −1 child.
* Nobody is their own child; a torus's two children differ; its two parents differ; the
  family is connected (finite, so generational loops close).

## A counting fact

In a closed family, every tube has one parent end and one child end. With exactly two parents
per torus there are 2n tubes, so the average number of children is exactly 2. Since charge
balance needs at least 2 children, **every torus has exactly 2 children**. Tori with 3 or 4
children need some tori to have more than two parents.

## Smallest families under each version of the rules

| version | smallest family | families at that size |
|---|---|---|
| basic | 3 tori | 1 |
| no torus is the child of its own child | 5 | 2 |
| sibling rule (two tori with the same two parents may not co-parent) | 3 | 1 |
| both of the above | 5 | 2 |
| half-sibling rule (tori sharing any parent may not co-parent), no 2-step loops | 8 | 18 |
| **dual tetrahedron** (both parents come from the other half), no 2-step loops | **8** | **4** |
| **dual tetrahedron**, no 2-step loops, **sibling rule** | **8** | **2** |
| dual tetrahedron, no 2-step loops, half-sibling rule | none up to 8 | — |

Counts are up to relabelling, searched exhaustively for 3 to 8 tori.

## The two dual-tetrahedron families on 8 tori

* The tori split into two tetrahedra of four. Every tube crosses between them, so generations
  alternate between the two tetrahedra.
* **Every torus is connected to all four tori of the other tetrahedron**: two are its children
  (+1 and −1) and two are its parents (mother and father).
* The shortest generational loop has length 4: A → B → A → B → back.
* The two families differ in how the + tubes link up. In one they form two loops of four, in
  the other a single loop through all eight. The − tubes do the same.

## Notes

* The sibling rule is what cuts 4 families to 2. The strict half-sibling rule leaves none,
  so loosening is needed for closure, as anticipated.
