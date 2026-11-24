# Claude-Creations
What i develop in Claude

## relational-geometry/ — Torus Porous

A navigable domain of relational geometry built from *Relational Geometry: Holes, Memory and the Internal Observer*.
Open `relational-geometry/index.html` in a browser (it loads Three.js r128 from cdnjs).

The world is the inside of a sponge, ray-marched as a union of gyroid tunnel networks at six nested scales (λ = 3). Every tunnel wall is perforated by the tunnels of the next scale, and those walls by the next. Each hole is the mouth of a tunnel that continues on, not a puncture in a sheet.

- **Hyperbolic travel.** Your size follows your distance to the walls, and your speed is measured in body lengths. As you approach a wall you shrink until its pores become passages. Going through one renormalizes the coordinates by λ: the scale sheds its coarsest layer and grows a finer one. Every 5 steps σ turns over (D1).
- **Stability grows with size.** Every scale orbits a **nexus**, a large ring-shaped hole that holds still. A scale's angular speed rises as it gets smaller (×√3 per step). The two largest visible scales are nearly still, and neighbouring scales counter-rotate. The smallest holes flicker open and shut: they are too small to sustain themselves. Each new depth forms its own nexus, so tori nest inside holes.
- **Gaze.** Where the pointer rests (or the screen centre on touch) is where you look. Each direction keeps a clock that runs at 15% while you look at it, so that region falls behind (up to 12 s) and tints cool. When you look away, its clock runs fast until it catches up.
- **Drift (T).** Still, slow (default, 0.2×) or flow (1×).
- **Elastic medium.** Space is warped hyperbolically around a point just ahead of you along your motion. Holes stretch open as you approach, and you can squeeze closer to walls than your own size.
- **Grading for navigation.** Near walls are pale bone, middle distance is sea-glass teal, and depth falls to near black, so every hole reads as a dark opening framed by a lit rim. Silhouettes are outlined in ink and pore throats darken. The nexus is gold.
- **Eversion (X)** passes through your own centre from motion into memory. The field slows to stillness and turns violet. Inside, the still field shows only where the present no longer matches what you remember, and those places glow. When you come back out, the change you missed plays out all at once, and S compares memory with the present.
- **Observer = (F_prev, F_now).** Probe rays measure the surrounding walls in body lengths. The everted memory field and the recurrence plot are drawn from those measurements.
- **Frame.** Keys 1–4 make 120° tetrahedral turns, and G is tracked as a spinor (g³ = −1, g⁶ = 1). Roll widens or narrows the pores.
