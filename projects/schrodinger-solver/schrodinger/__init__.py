"""A small, well-tested 1-D Schrödinger equation solver.

Two complementary solvers, both in natural units (``hbar = m = 1`` by default):

* :mod:`schrodinger.tise` — the *time-independent* equation. Builds a
  finite-difference Hamiltonian for an arbitrary potential and returns its
  bound-state spectrum (energies and wavefunctions).
* :mod:`schrodinger.tdse` — the *time-dependent* equation. Propagates a
  wavepacket with the split-step Fourier method, which is unitary to machine
  precision and therefore conserves the norm exactly.

Everything is validated against closed-form results in :mod:`schrodinger.analytic`.
"""

from . import analytic, potentials
from .tdse import SplitStepSolver, gaussian_wavepacket
from .tise import Eigenstates, build_grid, hamiltonian, solve

__all__ = [
    "analytic",
    "potentials",
    "build_grid",
    "hamiltonian",
    "solve",
    "Eigenstates",
    "SplitStepSolver",
    "gaussian_wavepacket",
]

__version__ = "0.1.0"
