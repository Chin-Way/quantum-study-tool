"""Common 1-D potentials ``V(x)``, in natural units (``hbar = m = 1`` by default).

Each factory returns a *vectorized* callable so it can be evaluated on a NumPy
grid and dropped straight into the Hamiltonian, e.g.::

    x, dx = build_grid(-10, 10, 2000)
    V = potentials.harmonic(omega=1.0)
    states = solve(x, V, k=5)
"""

from __future__ import annotations

from typing import Callable

import numpy as np

Potential = Callable[[np.ndarray], np.ndarray]


def free() -> Potential:
    """Free particle / infinite square well, ``V(x) = 0``.

    On a finite grid the domain edges act as infinite walls (the solver imposes
    ``psi = 0`` there), so ``free`` on ``[x_min, x_max]`` *is* the particle in a
    box.
    """
    return lambda x: np.zeros_like(x, dtype=float)


def harmonic(omega: float = 1.0, m: float = 1.0) -> Potential:
    """Quantum harmonic oscillator, ``V(x) = 1/2 m omega^2 x^2``."""
    return lambda x: 0.5 * m * omega**2 * x**2


def finite_well(depth: float, width: float, x0: float = 0.0) -> Potential:
    """Square well of given ``depth`` (>0) and ``width``, centered at ``x0``.

    ``V = -depth`` inside the well and ``0`` outside.
    """
    half = width / 2.0
    return lambda x: np.where(np.abs(x - x0) <= half, -abs(depth), 0.0)


def barrier(height: float, width: float, x0: float = 0.0) -> Potential:
    """Rectangular barrier of given ``height`` and ``width`` centered at ``x0``."""
    half = width / 2.0
    return lambda x: np.where(np.abs(x - x0) <= half, float(height), 0.0)


def double_well(a: float = 1.0, b: float = 4.0) -> Potential:
    """Symmetric quartic double well, ``V(x) = a x^4 - b x^2``.

    The classic toy model for tunneling between two minima and for the
    near-degenerate symmetric/antisymmetric ground-state doublet.
    """
    return lambda x: a * x**4 - b * x**2


def linear(field: float = 1.0) -> Potential:
    """Linear potential ``V(x) = field * x`` (a charged particle in a field)."""
    return lambda x: field * x
