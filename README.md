# Claude-Creations
What i develop in Claude

## ε-horn torus counting

* `viewer/torus_observer.html`: interactive viewer (phone friendly).
* `torus_count/`: the model written without external time; the system's own poloidal phase is the clock.
* `tests/`: known-result checks and the relational-time tests (`python3 -m pytest -q`).
* `experiments/relational_check.py` and `results/relational_check.md`: does anything depend on an absolute time?

Requires Python 3 with numpy (and pytest for the tests).
