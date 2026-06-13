"""Closed-form references used to validate the numerical solver.

Keeping the analytic answers next to the code makes the tests honest: the
numerical spectra are checked against these formulas, not against previously
recorded numbers.
"""

from __future__ import annotations

import numpy as np


def isw_energies(n, L: float, hbar: float = 1.0, m: float = 1.0):
    """Infinite square well of width ``L``.

    ``E_n = n^2 pi^2 hbar^2 / (2 m L^2)`` for ``n = 1, 2, 3, ...``.
    """
    n = np.asarray(n, dtype=float)
    return (n**2 * np.pi**2 * hbar**2) / (2.0 * m * L**2)


def qho_energies(n, omega: float = 1.0, hbar: float = 1.0):
    """Quantum harmonic oscillator.

    ``E_n = hbar omega (n + 1/2)`` for ``n = 0, 1, 2, ...``.
    """
    n = np.asarray(n, dtype=float)
    return hbar * omega * (n + 0.5)


def square_barrier_transmission(E, V0: float, a: float, hbar: float = 1.0, m: float = 1.0):
    """Transmission coefficient ``T(E)`` for a rectangular barrier.

    Barrier of height ``V0`` and width ``a``. Handles both tunneling
    (``E < V0``) and over-the-barrier (``E > V0``) regimes; the standard
    textbook result (e.g. Griffiths, *Introduction to Quantum Mechanics*).
    """
    E = np.atleast_1d(np.asarray(E, dtype=float))
    T = np.empty_like(E)

    below = E < V0
    above = E > V0
    equal = ~(below | above)

    # Tunneling regime: T = [1 + V0^2 sinh^2(kappa a) / (4 E (V0 - E))]^-1
    if np.any(below):
        Eb = E[below]
        kappa = np.sqrt(2.0 * m * (V0 - Eb)) / hbar
        T[below] = 1.0 / (1.0 + (V0**2 * np.sinh(kappa * a) ** 2) / (4.0 * Eb * (V0 - Eb)))

    # Over-the-barrier regime: replace sinh -> sin (resonances at sin = 0)
    if np.any(above):
        Ea = E[above]
        kp = np.sqrt(2.0 * m * (Ea - V0)) / hbar
        T[above] = 1.0 / (1.0 + (V0**2 * np.sin(kp * a) ** 2) / (4.0 * Ea * (Ea - V0)))

    # E == V0 limit (kappa -> 0): T = 1 / (1 + m V0 a^2 / (2 hbar^2))
    if np.any(equal):
        T[equal] = 1.0 / (1.0 + m * V0 * a**2 / (2.0 * hbar**2))

    return T if T.size > 1 else float(T[0])
