Create a new, from-scratch, portfolio-quality Python project named "percolation" that studies site and bond percolation on a 2-D square lattice, with a custom union-find (weighted quick-union with path compression) cluster detector written in NumPy. Build it in the current repository. If the repo already contains sibling projects under a projects/ directory, create this one alongside them as projects/percolation/; otherwise create a self-contained project directory named percolation/. Match the tone, structure, and rigor of a well-kept scientific-computing portfolio repo: clean vectorized code, docstrings, reproducible seeds, tests that check the physics (not merely that code runs), runnable example scripts that save figures, and honest, understated prose.

WHAT THIS PROJECT IS ABOUT
Percolation is the canonical model of a geometric phase transition. Occupy each site of an L x L square lattice independently with probability p (site percolation), or occupy each nearest-neighbor bond with probability p (bond percolation). Occupied neighbors form clusters. Below a critical occupation p_c the largest cluster is small and local; above p_c a single "spanning" cluster reaches from one side of the lattice to the other. As L grows the transition sharpens into a step. This is a clean, visual, self-contained showcase of critical phenomena and of an efficient classic algorithm (union-find) doing real scientific work.

Use periodic-free (open) boundaries and define spanning as: a single cluster touches both the top row and the bottom row (top-to-bottom / vertical spanning). Keep the spanning convention consistent everywhere.

THE PHYSICS YOU MUST GET RIGHT (state these precisely in code, tests, and README)
- Site-percolation threshold on the 2-D square lattice: p_c is approximately 0.5927 (0.592746...). This is a numerically known constant, not exact. Store it as a named constant, e.g. PC_SITE = 0.5927.
- Bond-percolation threshold on the 2-D square lattice: p_c = 1/2 exactly (Kesten's exact result). Store it as PC_BOND = 0.5.
- Correlation-length critical exponent for 2-D percolation: nu = 4/3 (approximately 1.333). Store as NU = 4.0 / 3.0.
- Order-parameter exponent: beta = 5/36 (approximately 0.139). Fractal dimension of the spanning cluster at p_c: D_f = 91/48 (approximately 1.896). Include these as documented constants; use D_f only in the stretch goal.
- Spanning (crossing) probability, which I will call Pi(p, L): the probability that a spanning cluster exists. It rises from ~0 to ~1 across p_c, and the curves for different L cross near p_c. For an L x L square with vertical spanning, the crossing value at p_c is close to 0.5. As L grows the curve steepens toward a step at p_c (finite-size scaling), with transition width shrinking like L^(-1/nu).
- Order parameter (largest-cluster fraction) P(p, L) = (size of the largest cluster) / L^2: it is ~0 well below p_c and rises toward ~1 as p -> 1 (at p = 1 the whole lattice is one cluster of size L^2). Report both the largest-cluster fraction of all sites (-> 1 as p -> 1) and, if useful, the fraction of occupied sites in the largest cluster.

PRIMARY GOAL
Implement, from scratch, a correct and reasonably fast percolation study for SITE percolation on the 2-D square lattice:
1. A union-find data structure: weighted quick-union with path compression, as its own module (for example percolation/unionfind.py) exposing a small clean class with find, union, connected, and a count of disjoint sets, plus the weights/sizes so you can report cluster sizes. Keep it pure NumPy / plain Python and O(alpha) amortized per operation.
2. A lattice module (for example percolation/lattice.py) that: generates a random occupied L x L boolean lattice at probability p from a seeded numpy Generator; builds clusters by unioning occupied nearest-neighbor pairs through the union-find; returns a cluster-label array, cluster sizes, the largest cluster, and a boolean for whether any cluster spans top-to-bottom.
3. A measurement module (for example percolation/measure.py) that, averaging over many seeded trials, computes: the spanning probability Pi(p, L) on a grid of p; the largest-cluster-fraction order parameter P(p, L); and an estimate of p_c as the p where Pi crosses 1/2 (linear interpolation between grid points). Expose the physics constants (PC_SITE, PC_BOND, NU, BETA, D_F) at the package level.

Validate in tests/ with pytest (check the science, with seeded RNG and modest sizes so CI stays fast, roughly under a couple of minutes):
- Union-find correctness on a hand-built example: after a known sequence of unions the connected components, set count, and component sizes are exactly right; find is stable/idempotent after path compression; total of all set sizes equals number of elements.
- Cluster-labeling correctness: the sum of all cluster sizes equals the number of occupied sites, for random lattices at several p and seeds. As an independent cross-check, compare your union-find cluster count and largest-cluster size against scipy.ndimage.label (4-connectivity) on the same occupied lattice and require they agree exactly.
- p = 1 (fully occupied) always spans, forms exactly one cluster of size L^2, and largest-cluster fraction = 1. p = 0 (empty) never spans, has zero clusters, and largest-cluster fraction = 0.
- Well below threshold (p = 0.3) the spanning probability is near 0 (for example below 0.1 at L around 32-64 over enough trials); well above threshold (p = 0.8) it is near 1 (above 0.9).
- Monotonicity: Pi(p, L) is non-decreasing across an increasing p grid (allow tiny statistical tolerance).
- Threshold recovery: the estimated site p_c (Pi = 1/2 crossing) is within about 0.03 of 0.5927 for L around 48-64 with a few hundred seeded trials.
- The named constants are correct: PC_SITE within 1e-3 of 0.5927, PC_BOND == 0.5 exactly, NU within 1e-9 of 4/3.

SECONDARY GOAL
- Add BOND percolation on the same square lattice (occupy edges, union the two endpoints of each occupied bond) and show its threshold is the exact value 1/2. Add a test that the estimated bond p_c (Pi = 1/2 crossing) is within about 0.03 of 0.5. Reuse the same union-find and spanning machinery.
- Add a finite-size-scaling demonstration in code and tests: the transition width narrows as L grows. Define a width (for example the p-interval over which Pi goes from 0.2 to 0.8, or the reciprocal of the maximum slope) and assert width(large L) < width(small L) for two sizes such as L = 16 vs L = 64.
- Provide a data-collapse helper: rescale the horizontal axis as x = (p - PC_SITE) * L**(1.0/NU); when Pi is plotted against x, curves for different L should collapse onto one scaling function. Include a test that the rescaled curves agree within a modest tolerance (interpolate to common x points and bound the spread).

STRETCH (only after PRIMARY and SECONDARY are solid and green)
- Measure the spanning-cluster fractal dimension at p_c: at p = PC_SITE the mass of the spanning cluster scales as L**D_f; fit log(mass) vs log(L) across several L and check the fitted exponent is near 91/48 (approximately 1.896) within a loose tolerance (for example plus/minus 0.1). Keep this test tolerant since it is statistically noisy.
- Optionally add a small animation (using Pillow or matplotlib) sweeping p from below to above p_c and watching the giant cluster appear, saved into figures/.

EXAMPLES (runnable demo scripts under examples/, each saving figures into a figures/ directory at the project root)
- examples/cluster_maps.py: render colored cluster maps for three occupations, below / at / above threshold (for example p = 0.45, p = 0.5927, p = 0.75), each site colored by its cluster label with a randomized colormap, and the spanning cluster highlighted. Save figures/cluster_maps.png. This is the money shot for the README.
- examples/spanning_curves.py: compute and plot Pi(p, L) versus p for several sizes (for example L = 16, 32, 64, 128), showing the step sharpening and the curves crossing near p_c; mark PC_SITE with a vertical line. On the same figure or a second panel, plot the largest-cluster-fraction order parameter rising from ~0 to ~1. Save figures/spanning_probability.png. Print the estimated p_c per L to stdout.
- examples/fss_collapse.py: show the raw Pi(p, L) curves and, beside them, the data collapse of Pi versus (p - p_c) * L**(1/nu) onto one curve. Save figures/fss_collapse.png.
Every example must run headless: set matplotlib to the Agg backend, create the figures/ directory if missing, make figures/ resolve relative to the script location, and use a fixed seed so figures are reproducible. Keep example runtimes to a minute or two.

REQUIRED PROJECT STRUCTURE AND FILES
- A source package directory (percolation/) containing __init__.py (with a short module docstring, re-exports of the key public functions and the physics constants, and __version__ = "0.1.0"), unionfind.py, lattice.py, and measure.py. Give modules clear docstrings that state the model and the constants.
- tests/ using pytest, with the science checks listed above, split into sensible files (for example tests/test_unionfind.py, tests/test_site.py, tests/test_bond.py, tests/test_fss.py). Use seeded RNGs everywhere and small enough sizes/trial counts that the full suite runs quickly.
- examples/ with the three runnable demo scripts above, writing into figures/.
- README.md in an honest, understated tone. Open with the one-line idea, then explain the method (site vs bond percolation, union-find as the cluster detector, spanning definition, how Pi and the order parameter are measured), state the physics targets precisely (p_c approximately 0.5927 for site, exactly 0.5 for bond, nu = 4/3, the crossing near p_c, the step sharpening with L, the order parameter going 0 -> 1), report the numbers your own runs actually produced, and embed at least one figure (the cluster maps and/or the spanning-probability curves). Include a short Quickstart (pip install -r requirements.txt; python -m pytest -q; then the example commands), a small "How it works" section, a "Project layout" section, and a References section (Stauffer and Aharony, Introduction to Percolation Theory; Kesten on the exact bond threshold; Newman and Ziff on efficient percolation algorithms; Sedgewick and Wayne on weighted quick-union with path compression). Do not overclaim; write like an engineer documenting real results. Do not paste fake numbers, run the examples and quote what you actually got.
- requirements.txt with lightweight pinned deps: numpy>=1.24, scipy>=1.10, matplotlib>=3.7, pytest>=7.0 (add pillow>=10.0 only if you build the optional animation). No deep-learning frameworks; scikit-learn is not needed here.
- pyproject.toml using the setuptools build backend, project name "percolation", version 0.1.0, requires-python >=3.10, MIT license, dependencies listed, a dev extra with pytest, [tool.setuptools] packages = ["percolation"], and [tool.pytest.ini_options] with pythonpath = ["."] and testpaths = ["tests"].
- LICENSE: the MIT License, "Copyright (c) 2026 Wei Chen" to match the sibling projects in this repo.
- .gitignore covering __pycache__/, *.pyc, .pytest_cache/, *.egg-info/, .venv/, venv/, and generated figures if you prefer (but do commit at least the one or two figures the README embeds so the README renders on GitHub).
- A GitHub Actions CI workflow at .github/workflows/ci.yml (path relative to the project root) named "tests", triggering on push and pull_request, running on ubuntu-latest across a Python matrix of 3.10, 3.11, and 3.12, checking out the code, setting up Python, installing with pip install -r requirements.txt, and running python -m pytest -q.

QUALITY BAR
- Tests assert real physics and algorithm correctness with named constants and tolerances, not just "it ran without error". Every numeric assertion should correspond to a stated fact above.
- Code is vectorized where it naturally is (lattice generation, neighbor enumeration), clean, typed where helpful, and documented. The union-find is a genuine weighted quick-union with path compression, not a wrapper around a library. Prefer building the occupied-neighbor pair list with array operations, then unioning.
- Everything is reproducible: seeded numpy Generators throughout; the same seed gives the same figures and the same test outcomes.
- The full pytest suite passes locally and is fast enough for CI. Examples run headless and actually produce the figures the README references. The README's quoted numbers come from real runs.
- Keep dependencies to numpy, scipy, matplotlib, pytest (plus pillow only if you add the animation).

WORKFLOW
- Work on a branch (create one), unless the repository is empty, in which case you may work directly on main.
- Make small, logical commits (for example: scaffold and packaging; union-find plus its tests; site lattice and clustering; measurement and threshold estimate; bond percolation; FSS and collapse; examples and figures; README; CI). Write clear commit messages.
- Run the tests before each commit and only commit when they pass.
- Do NOT open a pull request unless I explicitly ask for one.
- When finished, end with a concise summary of what you built, the project layout, the physics numbers your runs produced (estimated site p_c, bond p_c, how the curves sharpen with L), and the final pytest results.
