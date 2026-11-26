# Rules of the lineage (draft 1)

A precise statement of the parent → child → grandparent picture, so that every
configuration that spawns and closes can be listed by a program.

## Objects

* **Parent.** A torus with two loops: `a` (toroidal, around the big circle) and
  `b` (poloidal, through the hole).
* **Vortices.** Points on the parent. A vortex of charge `p/t` (lowest terms)
  is a place where the phase turns `p/t` of the wheel on one trip around it.
* **Children.** The lineage has `d` children in total. Each child is one sheet
  lying over the parent: every point of the parent has `d` children above it.
* **Spikes.** Each vortex joins the children above it into cycles. A cycle of
  length `t` is one child horn torus of winding `(t, p)`: it closes after `t`
  trips around the vortex, having turned the phase `p` times.

## Moves

Walking once along a loop of the parent carries each child to some child. So
every loop gives a shuffle (a permutation) of the `d` children:

* `A` for the toroidal loop `a`, `B` for the poloidal loop `b`,
* `S_i` for the small loop around vortex `i`.

A vortex of charge `p/t` with a single child of winding `(t, p)` shuffles `t`
children in a cycle and leaves the other `d − t` alone.

## When a configuration closes

Going around all the vortices together is the same as going around the parent's
two loops forward and then backward (on a torus that big loop is the rim
`a b a⁻¹ b⁻¹`). The lineage **closes** when doing all of it returns every child
to itself:

    A B A⁻¹ B⁻¹ · S₁ S₂ ⋯ S_k = do nothing

and it is **one family** when every child can be reached from every other by
these moves.

Two configurations are the same if they differ only by renaming the children.

## Two versions of the shuffles

* **Phase-wheel version.** The children are the `d` phase offsets
  `0, 1/d, …, (d−1)/d`, and every move rotates them (a charge `q` shifts every
  child by `q`). All moves commute.
* **General version.** Any shuffles at all, as long as each vortex's shuffle has
  the cycle lengths its charges call for.

## What gets counted

For each choice of `d` and vortex types, the number of closed families, each
weighted by 1 / (number of renamings that leave it unchanged). This is the
standard way to count covers, called a Hurwitz number, so the results can be
compared with known mathematics.

The total number of holes of a closed lineage follows from the Riemann–Hurwitz
formula over a torus: `2g − 2 = Σ_i (d − number of cycles of S_i)`.
