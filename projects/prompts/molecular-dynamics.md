Create a new, from-scratch, portfolio-quality Python project called `molecular-dynamics`: a Lennard-Jones molecular-dynamics simulation of a 2-D (default) and optionally 3-D gas/liquid, written in pure NumPy. This is a standalone scientific-computing repository meant to sit alongside sibling projects (schrodinger-solver, quantum-algorithms, ml-ising-phases) and must match their style: a clean source package, physics-validating pytest tests, runnable example scripts that save figures, an honest and understated README that embeds a figure, and CI. Work in the current empty repository/directory.

Match this exact layout and conventions:

  molecular-dynamics/
    mdlj/                       # the source package (import name: mdlj)
      __init__.py               # module docstring + clean public API in __all__, __version__ = "0.1.0"
      potential.py             # LJ 12-6 potential and pair force, with cutoff + energy shift
      simulation.py            # System/Simulation class: state, PBC box, minimum-image, run loop
      integrator.py            # velocity-Verlet step
      neighbors.py             # linked cell list / Verlet neighbor list for O(N) force evaluation
      observables.py           # kinetic/potential energy, instantaneous temperature, g(r), speed histogram, virial pressure
      thermostat.py            # Berendsen (and optionally Andersen) thermostat for NVT
      initialize.py            # lattice position init + Maxwell-Boltzmann velocity init (zero net momentum, exact target T)
      analytic.py              # closed-form references: Maxwell-Boltzmann speed distributions, equipartition, ideal-gas relations
      plotting.py              # headless-safe figure helpers (set matplotlib Agg backend)
    examples/
      nve_energy_demo.py        # NVE run; plot total/kinetic/potential energy vs time; print energy drift and fluctuation
      gofr_demo.py              # equilibrate a liquid; compute and plot g(r)
      maxwell_boltzmann_demo.py # equilibrate; histogram of speeds vs the analytic curve
      animation_demo.py         # animate the particles; save a GIF into figures/ via Pillow
    tests/                      # pytest, checking the SCIENCE (see below), not just "it runs"
    figures/                    # written by the example scripts (committed once generated)
    README.md
    requirements.txt
    pyproject.toml
    LICENSE                     # MIT, "Copyright (c) 2026 Wei Chen"
    .gitignore                  # __pycache__/, *.pyc, .pytest_cache/, *.egg-info/, .venv/, venv/
    .github/workflows/ci.yml

Dependencies stay lightweight: numpy, scipy (for stats such as a KS test and special functions in analytic references), matplotlib, pillow (for the GIF), and pytest. No scikit-learn, no deep-learning frameworks. Support Python >= 3.10. The pyproject.toml uses the setuptools build backend, lists the runtime deps, a [project.optional-dependencies] dev = ["pytest>=7.0"], packages = ["mdlj"], and [tool.pytest.ini_options] with pythonpath = ["."] and testpaths = ["tests"]. requirements.txt lists numpy>=1.24, scipy>=1.10, matplotlib>=3.7, pillow>=10.0, pytest>=7.0. The CI workflow at .github/workflows/ci.yml is named "tests", triggers on push to main and on pull_request, uses a matrix of Python 3.10, 3.11, 3.12 on ubuntu-latest, installs with `pip install -r requirements.txt`, and runs `python -m pytest -q`. Example scripts must add the project root to sys.path so they run as `python examples/<name>.py`, create figures/ if missing, write PNG/GIF there, and print validation tables/numbers to stdout.

Work in reduced Lennard-Jones units throughout: set epsilon = sigma = m = k_B = 1, so temperature is measured in units of epsilon/k_B and the time unit is tau = sigma*sqrt(m/epsilon). State this in the README and docstrings.

===================================================================
PRIMARY GOAL  (must fully implement, validate with tests, and visualize)
===================================================================

1. Lennard-Jones interaction. Implement U(r) = 4*epsilon*[(sigma/r)^12 - (sigma/r)^6]. The potential has its minimum at r_min = 2^(1/6)*sigma (approximately 1.122462*sigma) where U(r_min) = -epsilon and the force is exactly zero. Implement the pair force as the negative gradient: magnitude F(r) = (24*epsilon/r)*[2*(sigma/r)^12 - (sigma/r)^6], applied as the vector F_ij = 24*epsilon*[2*(sigma/r)^12 - (sigma/r)^6]*(r_ij / r^2). Use a cutoff radius r_c = 2.5*sigma and shift the potential so that U_shift(r) = U(r) - U(r_c) for r < r_c and 0 beyond, making the energy continuous (equal to zero) at the cutoff; note that the unshifted U(2.5*sigma) is approximately -0.0163*epsilon.

2. Periodic boundary conditions with the minimum-image convention. Particles live in a square (2-D) or cubic (3-D) box of side L with PBC. Compute pair separations with the minimum image: for each component, dx -> dx - L*round(dx/L), so every component lands in [-L/2, L/2]. Forces obey Newton's third law (F_ij = -F_ji), so the total force on the system sums to zero.

3. Velocity-Verlet integration (NVE / microcanonical). One step: x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2; compute a(t+dt) from the new positions; v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt. This integrator is second-order accurate and time-reversible/symplectic, which is why total energy is conserved (bounded fluctuations, no secular drift) and total linear momentum is conserved exactly to floating-point precision.

4. Cell list / neighbor list for efficiency. Implement a linked-cell list (cells of side >= r_c) and/or a Verlet neighbor list so force evaluation is O(N) rather than O(N^2). It must produce forces and energies identical to the brute-force O(N^2) computation.

5. Initialization. Place particles on a lattice (square or triangular in 2-D, FCC in 3-D) to avoid overlaps; draw velocities from a Gaussian (Maxwell-Boltzmann) at the target temperature; subtract the center-of-mass velocity so net momentum is zero; rescale velocities so the initial instantaneous temperature exactly equals the target.

6. Core observables. Kinetic energy KE = 0.5*sum(m*v^2); potential energy from the shifted LJ; instantaneous temperature from equipartition, T = 2*KE/(N_dof*k_B), with N_dof = d*N - d (subtracting the d center-of-mass degrees of freedom). Radial distribution function g(r) accumulated via a histogram of minimum-image pair distances, normalized by the ideal-gas shell count rho*shell_volume so that g(r) -> 1 at large r. Speed distribution as a normalized histogram.

Validate the PRIMARY GOAL with pytest tests that assert physics, for example:
  - test_potential: U(2^(1/6)) == -1 within 1e-12; F(2^(1/6)) == 0 within 1e-9; the analytic force matches a central finite-difference of U(r) to rtol <= 1e-5; U_shift(r_c) == 0 exactly and is continuous at the cutoff.
  - test_forces: total force over all particles sums to zero to atol <= 1e-10; F_ij == -F_ji; minimum-image displacements all lie in [-L/2, L/2]; cell-list/neighbor-list forces and total energy match the brute-force O(N^2) result to atol <= 1e-10.
  - test_conservation: over an NVE run of at least 10^4 steps at dt = 0.005*tau, the relative total-energy fluctuation std(E)/abs(mean(E)) < 1e-3 and the relative drift abs(E_final - E_initial)/abs(E_initial) < 1e-2; total linear momentum stays constant with abs(P(t) - P(0)) < 1e-10 throughout.
  - test_equipartition: after equilibration the measured temperature T = 2*KE/(N_dof*k_B) equals the target to within 5%, and the per-component velocity variance equals k_B*T/m to within 5%.

Visualize the PRIMARY GOAL: nve_energy_demo.py produces an energy-vs-time plot showing total energy flat while KE and PE exchange, and prints the measured energy drift and fluctuation. This figure is embedded in the README.

===================================================================
SECONDARY GOAL
===================================================================

1. Radial distribution function g(r) for a liquid. Equilibrate an LJ liquid at a standard state point (in 3-D use reduced density rho* = N/V approximately 0.8 and temperature T* approximately 1.0; in 2-D use rho* approximately 0.7 and T* approximately 1.0), then accumulate g(r) over many frames. It must show the characteristic liquid structure: g(r) ~ 0 for r below about 0.9*sigma (excluded volume), a strong first peak near r approximately 1.1*sigma, decaying oscillations, and g(r) -> 1 at large r. As a sanity check, a low-density (ideal-gas-like) run must give g(r) approximately 1 for all r. Test: the tail average of g(r) is within 10% of 1; g(r) < 0.1 for r < 0.9*sigma; the first-peak location falls between 1.0 and 1.3*sigma; and the low-density g(r) is 1 within about 10%. gofr_demo.py saves a g(r) plot into figures/.

2. Maxwell-Boltzmann speed distribution at equilibrium. The equilibrium velocity components are Gaussian with mean 0 and variance k_B*T/m. In 2-D the speed distribution is the Rayleigh form f(v) = (m*v/(k_B*T))*exp(-m*v^2/(2*k_B*T)) with mean speed <v> = sqrt(pi*k_B*T/(2*m)), most-probable speed v_p = sqrt(k_B*T/m), and rms speed v_rms = sqrt(2*k_B*T/m). In 3-D it is f(v) = 4*pi*v^2*(m/(2*pi*k_B*T))^(3/2)*exp(-m*v^2/(2*k_B*T)) with <v> = sqrt(8*k_B*T/(pi*m)), v_p = sqrt(2*k_B*T/m), v_rms = sqrt(3*k_B*T/m). Provide these analytic curves in analytic.py. maxwell_boltzmann_demo.py overlays the simulated speed histogram on the analytic curve and saves the figure. Test: the measured mean speed matches the analytic value to within 5%; the measured v_rms matches sqrt(d*k_B*T/m) to within 5%; and a scipy KS or chi-square test of the sampled speeds against the analytic distribution does not reject the fit (p > 0.05, or a small statistic).

3. NVT thermostat. Implement a Berendsen thermostat with velocity rescale factor lambda = sqrt(1 + (dt/tau_T)*(T_target/T - 1)) (optionally also an Andersen thermostat that stochastically reassigns velocities from the Maxwell-Boltzmann distribution at a chosen collision rate). Test: starting from a temperature well away from the target, the thermostat drives the time-averaged temperature to within 5% of T_target after equilibration.

4. Animation. animation_demo.py renders the moving particles (a scatter animation of positions in the box) and saves a GIF into figures/ using the Pillow writer, so it works headlessly.

===================================================================
STRETCH  (only after PRIMARY and SECONDARY are solid and green)
===================================================================

  - Virial pressure. Compute the instantaneous pressure via the virial P = rho*k_B*T + (1/(d*V))*<sum_{i<j} r_ij . F_ij>, and check that in the low-density limit it reduces to the ideal-gas law P -> rho*k_B*T within a few percent.
  - g(r) coordination check: verify the normalization by confirming that rho times the integral of g(r) over the shell volume recovers the expected neighbor count (integrates toward N-1 over the whole box).
  - A simple melting/structure sweep: scan temperature at fixed density and show the first g(r) peak sharpening/broadening (solid vs liquid vs gas), summarized in a figure.
  - Optional 3-D support with an FCC initial lattice, exercised by at least one test.
  - Long-range tail correction to energy/pressure for the truncated potential.

===================================================================
QUALITY BAR
===================================================================

  - Physics-first tests. Every test must assert a physical/mathematical fact with a concrete numerical tolerance (as above), comparing against a closed-form reference in analytic.py or against the brute-force implementation, never merely that a function returns without error. Aim for a comparable footprint to the sibling repos (roughly 10-15 meaningful tests). Tests must be deterministic: seed all randomness (np.random.default_rng(seed)) and keep each test fast (small N, few steps) so the whole suite runs in well under a minute in CI.
  - Vectorized NumPy. No Python-level double loops over particle pairs in the hot path; use vectorized array operations and the cell/neighbor list. Keep the code readable and documented.
  - Honest, understated README.md in the style of the sibling projects: a short intro stating what it does and does not do; a "Why this project" paragraph; a "Highlights" list; a "Results" section with the actual measured numbers (energy drift/fluctuation, measured vs target temperature, g(r) peak location, mean-speed agreement) and at least one embedded figure (for example ![NVE energy conservation](figures/energy_conservation.png)); a "Quickstart" with pip install and the pytest/example commands; a "How it works" section with the LJ potential, velocity-Verlet update, minimum-image/PBC, and the cell list; a "Project layout" tree; a "References" list (e.g. Allen & Tildesley, Computer Simulation of Liquids; Frenkel & Smit, Understanding Molecular Simulation; Verlet 1967); and a "License" line. Do not overclaim; report real numbers produced by the example scripts.
  - Docstrings on every public function/class explaining the physics and the units. Module docstring in __init__.py summarizing the package and its reduced units.
  - Headless-safe plotting: select the matplotlib Agg backend in plotting.py before importing pyplot so examples and CI never need a display.
  - Determinism and reproducibility: examples accept/print the seed they use.

===================================================================
WORKFLOW
===================================================================

  - If the repository is empty, work directly on the default branch (main); otherwise create and work on a feature branch. Do not commit onto someone else's in-progress branch.
  - Make small, logical commits (for example: project scaffolding + LICENSE/CI; LJ potential and force; PBC + minimum image; velocity-Verlet integrator; cell/neighbor list; initialization; observables and g(r); thermostat; examples and figures; README). Write clear commit messages.
  - Run the test suite (`python -m pytest -q`) before each commit and only commit when it is green. Also run the example scripts to generate the figures that the README embeds, and commit those figures.
  - Do NOT open a pull request unless explicitly asked.
  - When finished, end with a short summary of what was built and the final test results (the pytest output / pass count), plus the key validated numbers (energy conservation, temperature vs target, g(r) peak, mean-speed agreement).

Start by scaffolding the project (package, pyproject.toml, requirements.txt, LICENSE, .gitignore, CI), then implement and test the potential and forces, then the integrator and conservation laws, then the cell list, then the observables (g(r), speed distribution), then the thermostat, then the example scripts and README. Validate the physics at every step.
