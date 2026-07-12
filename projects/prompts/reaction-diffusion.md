Create a new, from-scratch, portfolio-quality Python project named `reaction-diffusion`: a 2-D reaction-diffusion solver that produces Turing patterns via the Gray-Scott model, vectorized in NumPy. This is a standalone repo meant to sit alongside sibling projects (schrodinger-solver, quantum-algorithms, ml-ising-phases) and must match their style: a clean source package, PHYSICS-validating pytest tests, figure/animation-saving examples, an honest understated README with an embedded figure, and CI. Work in the current empty repository.

STRUCTURE:
- package `rdsolver/`: laplacian.py (5-point periodic Laplacian), diffusion.py (pure-diffusion stepper + analytic Gaussian reference), grayscott.py (the two-species stepper), presets.py (named (feed, kill) parameter sets), plotting.py (headless Agg helpers). __init__.py exposes a clean public API and __version__ = "0.1.0".
- tests/ using pytest, checking the PHYSICS (see below).
- examples/ writing figures/GIFs into a figures/ directory at the project root.
- README.md; requirements.txt (numpy>=1.24, scipy>=1.10, matplotlib>=3.7, pillow>=10.0, pytest>=7.0); pyproject.toml (setuptools backend, packages = ["rdsolver"], pythonpath = ["."], testpaths = ["tests"], requires-python >=3.10); LICENSE (MIT, "Copyright (c) 2026 Wei Chen"); .gitignore; .github/workflows/ci.yml named "tests", on push + pull_request, matrix Python 3.10/3.11/3.12, `pip install -r requirements.txt`, `python -m pytest -q`. Examples run headless as `python examples/<name>.py`.

PRIMARY GOAL — a validated diffusion core (get this right BEFORE any reaction terms).
- Implement the discrete Laplacian with a 5-point stencil: lap(f) ~ (f_up + f_down + f_left + f_right - 4*f_center)/dx^2, with PERIODIC boundaries via np.roll. Implement explicit forward-Euler time stepping.
- VALIDATE pure diffusion df/dt = D*lap(f) against closed form:
    * Mass conservation: with periodic boundaries the total sum of the field is conserved to atol <= 1e-9 over many steps.
    * Gaussian spreading: a narrow Gaussian (or point) initial condition spreads as a Gaussian whose second moment grows LINEARLY in time. In 2-D, <r^2>(t) = <r^2>(0) + 4*D*t; fit <r^2> vs t and assert the slope equals 4*D within a few percent (measured well before the packet feels the periodic box).
    * Laplacian accuracy: the discrete Laplacian of a smooth test function such as sin(2*pi*x)*sin(2*pi*y) matches the analytic Laplacian, and the error decreases like O(dx^2) under grid refinement.
    * Stability: the explicit scheme is stable when D*dt/dx^2 <= 1/4 (the 2-D diffusion-number condition); a run at, e.g., D*dt/dx^2 = 0.2 stays bounded. (Optionally show that clearly violating the bound blows up.)

SECONDARY GOAL — Gray-Scott Turing patterns.
- Implement the Gray-Scott system on the periodic grid:
    du/dt = Du*lap(u) - u*v^2 + F*(1 - u)
    dv/dt = Dv*lap(v) + u*v^2 - (F + k)*v
  with typical Du = 0.16, Dv = 0.08, and named (F, k) presets for distinct Pearson morphologies, e.g. spots (F=0.035, k=0.065), mitosis / self-replicating spots (F=0.0367, k=0.0649), stripes/labyrinth (F=0.055, k=0.062). Initialize u=1, v=0 everywhere with a small seeded central square set to u=0.5, v=0.25 plus a little noise.
- Tests (framed to be robust, since exact morphology is qualitative): u and v stay finite and within sane bounds (about [0, 1]) throughout; starting from a near-uniform field a NONTRIVIAL pattern develops (the spatial standard deviation of v grows from ~0 to a substantial value); different presets yield statistically distinguishable textures (e.g. different final pattern variance or dominant wavelength) under fixed seeds.
- examples/pattern_growth.py animates a pattern emerging and saves figures/turing.gif (Pillow). examples/gallery.py runs several presets and saves a montage figures/gallery.png.

STRETCH (only after the above is green): a Brusselator or Gierer-Meinhardt model for comparison; a short linear-stability note deriving the Turing condition (why the uniform state destabilizes); or an implicit/ADI stepper that permits larger dt.

QUALITY BAR: fully vectorized (no per-cell Python loops); deterministic seeded RNG so patterns and figures reproduce exactly; roughly 10-15 tests dominated by the EXACT pure-diffusion checks plus robust pattern-emergence checks; fast in CI (small grid / few steps in tests, longer runs only in examples); honest README explaining diffusion, the Gray-Scott terms, the stability condition, and what each preset does, with an embedded pattern figure and the REAL measured numbers (fitted diffusion slope, stability threshold). Docstrings throughout; headless Agg plotting.

WORKFLOW: work on a branch (or main if the repo is empty); small logical commits (Laplacian + diffusion validation; Gray-Scott stepper; presets; examples + figures; README); run `python -m pytest -q` before each commit and only commit when green; run the examples to generate the embedded figures and commit them; do NOT open a pull request unless I ask. End with a short summary and the final test results.
