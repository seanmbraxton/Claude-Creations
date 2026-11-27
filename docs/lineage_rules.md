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

## Draft 3: two parental sides, as many parents as children

The rules that make 2, 3 or 4 (or more) children work:

1. **As many parents as children.** A torus with k vortices has k children and k parents.
2. **Two parental sides.** Parents arrive at the two ends of the child's axis: positive charges
   at one end (the mother's side), negative at the other (the father's side). With k = 2 this is
   exactly one mother and one father.
3. **The dual set.** The tori form two sets, A and B, and every parent comes from the other set
   (the dual tetrahedron, generalized).
4. **Balance.** Charges leaving a torus net zero, and so do charges arriving.
5. **No torus is the child of its own child.**
6. **Sibling rule.** Tori with identical parents never co-parent.

Consequence: a torus is linked to 2k different tori of the other set, so the smallest family has
**4k tori**: 8 for two children, 12 for three, 16 for four. A family reaching this bound exists for
every k (code: `torus_count/dual_families.py`; page: `viewer/dual_families.html`).

## Draft 4: inherited charge (current)

1. **Two parents.** Every torus has a mother and a father, one at each end of its axis, both
   from the dual set. Every torus has two children (the counting fact forces it).
2. **Every tube carries a charge**, the charge of the vortex it came from.
3. **Natural state.** A child's state is the sum of what its mother and father gave it:
   +1 and −1 give 0; +1 and −1/3 give 2/3.
4. **Pass on exactly what you inherited.** The charges a torus sends to its children add up to
   its natural state.
5. **The whole family balances.** The states of all tori add up to zero.
6. As before: nobody is the child of their own child, and tori with identical parents never
   co-parent.

Consequence: charge can only circulate around generational loops (Kirchhoff's current law). A
torus's state is the sum of the charges of the loops through it, and the family balances when
the sum over loops of (charge × loop length) is zero. Fractions come from balancing loops of
different lengths. Results: `results/exploration.md`.

## Draft 5: the sign is the winding direction

Added to draft 4:

7. **Sign = winding direction about the child's axis.** The mother's tube winds one way about
   the toroidal axis and carries a positive charge (or zero); the father's tube winds the other
   way and carries a negative charge (or zero).

Consequence: a negative charge moving forward along a father's tube is a positive charge moving
backward. Charge therefore circulates on zigzag loops: forward along maternal lines, backward
along paternal lines. A zigzag loop with f forward and b backward steps, carrying charge c,
adds c × (f − b) to the family's total. Loops with f = b balance themselves; the rest must
balance each other, and that sets the fractions.

## Draft 6: splits in superposition

Kept from the user's rules: horn torus as a continuous phase relation; a vortex spawns a child
through a spike (leaves along the surface normal, arrives along the child's axis); sign = local
direction of rotation; two parents, child starts at their sum; every child reconnects to its
grandparent through its own offspring; only closed generational loops net zero; branching is
addition.

New: rule 7 ("scaling decides stability") is not chosen. A twisted torus splits its imbalance of
M units among k children every way at once; child j sits where its vortex is, at angle theta_j,
and carries phase e^{i m_j theta_j}. The splits interfere; stable forms are the survivors.

Result (torus_count/interference.py, tests/test_interference.py): with evenly placed children,
the sum is exactly 1 in size when k divides M and exactly 0 otherwise. A prime imbalance
survives only whole or as all ones. The clean pattern needs each unit to wind the phase a whole
number of times; children whose arcs are sized by their charge never cancel.
