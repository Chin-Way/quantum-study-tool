Create a new, from-scratch, portfolio-quality Python project named `game-of-life`: Conway's Game of Life plus a small cellular-automata toolkit, vectorized in NumPy. This is a standalone repo meant to sit alongside sibling projects (schrodinger-solver, quantum-algorithms, ml-ising-phases) and must match their style: a clean source package, RULE-validating pytest tests (not just "it runs"), runnable example scripts that save figures/GIFs, an honest and understated README that embeds a figure, and CI. Work in the current empty repository.

STRUCTURE:
- package `life/`: grid.py (the CA engine), rules.py (named rulesets), patterns.py (a library of named patterns as cell coordinates), plotting.py (headless Agg-backend helpers). __init__.py exposes a clean public API in __all__ and __version__ = "0.1.0".
- tests/ using pytest, checking the RULES (see below).
- examples/ writing figures/GIFs into a figures/ directory at the project root.
- README.md; requirements.txt (numpy>=1.24, scipy>=1.10, matplotlib>=3.7, pillow>=10.0, pytest>=7.0); pyproject.toml (setuptools backend, packages = ["life"], [tool.pytest.ini_options] with pythonpath = ["."] and testpaths = ["tests"], requires-python >=3.10); LICENSE (MIT, "Copyright (c) 2026 Wei Chen"); .gitignore (__pycache__/, *.pyc, .pytest_cache/, *.egg-info/, .venv/, venv/); .github/workflows/ci.yml named "tests", on push + pull_request, matrix Python 3.10/3.11/3.12 on ubuntu-latest, `pip install -r requirements.txt`, `python -m pytest -q`. Examples run headless as `python examples/<name>.py`.

PRIMARY GOAL — a correct, fast Life engine.
- Represent the board as a 2-D boolean/uint8 NumPy array with TOROIDAL (periodic) boundaries. Compute the 8-neighbour live count with a vectorized convolution (scipy.signal.convolve2d with boundary='wrap', OR nine np.roll additions) — do NOT call a cellular-automata library. Apply Life's rule B3/S23: a dead cell with exactly 3 live neighbours is born; a live cell with 2 or 3 live neighbours survives; otherwise it dies.
- Ship a pattern library with correct coordinates for: block, beehive, loaf (still lifes); blinker, toad, beacon (period-2 oscillators); pulsar (period 3); glider; lightweight spaceship (LWSS); and the Gosper glider gun.
- VALIDATE THE RULES with deterministic pytest tests (these are EXACT, not statistical):
    * The vectorized neighbour count equals a brute-force per-cell neighbour count on random boards.
    * Still lifes (block, beehive, loaf) are unchanged after 1 and after many generations.
    * Blinker, toad, and beacon each return to their initial state after EXACTLY 2 generations and differ after 1. The pulsar returns after EXACTLY 3.
    * The glider is identical to its initial configuration translated by (+1, +1) after EXACTLY 4 generations (use a board large enough / toroidal that it does not interact with itself).
    * The LWSS returns to its shape displaced by 2 cells after EXACTLY 4 generations.
    * The Gosper glider gun's population is UNBOUNDED: over a window before any emitted glider wraps around the torus (use a large board), the gun emits exactly one new glider (5 live cells) every 30 generations — assert the population increases by 5 every 30 generations across the first few emissions.

SECONDARY GOAL — generalize the CA + visualize.
- Support arbitrary "B{birth}/S{survival}" rulestrings and provide named presets: Life (B3/S23), HighLife (B36/S23), Day & Night (B3678/S34678), Seeds (B2/S). Test that a rulestring round-trips (parse -> format -> parse) and that at least one non-Life preset produces its known short-term behaviour.
- examples/glider_gun.py animates the Gosper gun on a large board and saves figures/glider_gun.gif (Pillow writer). examples/oscillators.py renders a montage of the named patterns. examples/random_soup.py evolves a seeded random field and plots population vs generation, showing it settle toward still lifes/oscillators.

STRETCH (only after the above is green): Langton's ant (a different CA) with the famous "highway" emerging after ~10,000 steps; run-length-encoded (RLE) pattern import so any Life pattern from the wild can be loaded; or a still-life/oscillator census of random soups.

QUALITY BAR: vectorized (no Python double loop in the step); deterministic seeded RNG (np.random.default_rng) for random demos; roughly 10-15 rule-checking tests, all fast in CI; honest README explaining the rule, the convolution trick, and the patterns, with an embedded GIF/figure and the REAL observed numbers (e.g. the measured gun period). Docstrings on every public function/class. Headless-safe plotting (Agg backend selected before importing pyplot).

WORKFLOW: work on a branch (or main if the repo is empty); make small logical commits (engine; patterns; rule tests; rulesets; examples + figures; README); run `python -m pytest -q` before each commit and only commit when green; run the examples to generate the figures the README embeds and commit them; do NOT open a pull request unless I ask. End with a short summary of what was built and the final test results.
