# Rules of the lineage (draft 2, in the author's terms)

## The rules

1. **A horn torus is a continuous phase relation**, for example between time and state.
2. **A vortex is a place of localized phase change** on a torus's surface. Its charge can be
   whole or fractional.
3. **Every vortex spawns a child** horn torus. A tube leaves the vortex along the surface
   normal and arrives along the child's toroidal axis, into its horn point.
4. **Charge balance.** The vortex charges on each torus sum to zero. So every torus has at
   least two vortices, and therefore at least two children.
5. **The grandparent rule.** Every child must reconnect to its grandparent through its own
   offspring: if G spawned P and P spawned X, then X spawns G.
6. **Closure.** Spawning must eventually stop, so children are tori already in the family.
   A torus is never its own child, and one torus spawns another at most once.

## How the program reads them

A family is a directed graph on n tori, with an edge u → v when a vortex on u spawns v. Rules
4–6 become: every torus has out-degree at least 2 and in-degree at least 1; there are no
self-loops; and G → P → X forces X → G. Charges are numbers on the edges: those leaving a
torus sum to zero (rule 4), and optionally those arriving at a torus sum to zero too
(balance at the horn point).

For comparison the program also runs the **great-grandparent rule**: G → P → X → Y forces
Y → G.

Code: `torus_count/lineage.py`. Results: `results/lineage_closure.md`.

## Earlier draft

Draft 1 read the children as sheets of a branched cover of a single parent (Hurwitz
counting). Its results are kept in `results/lineage_enumeration.md`. That reading is a
different question from the one above.
