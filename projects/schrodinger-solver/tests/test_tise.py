"""The time-independent solver is checked against closed-form spectra."""

import numpy as np
import pytest

from schrodinger import analytic, build_grid, potentials, solve


def test_infinite_square_well_energies():
    """Particle in a box: E_n = n^2 pi^2 / (2 L^2) in natural units.

    The effective well width is (N+1)*dx because the Dirichlet zeros sit one
    grid step beyond the domain (see tise.py).
    """
    x, dx = build_grid(0.0, 1.0, 1999)
    states = solve(x, potentials.free(), k=5)

    L = states.effective_box_width()
    n = np.arange(1, 6)
    expected = analytic.isw_energies(n, L)

    assert np.allclose(states.energies, expected, rtol=2e-4)


def test_harmonic_oscillator_energies():
    """QHO: E_n = omega (n + 1/2). Ground state at 0.5, evenly spaced by omega."""
    omega = 1.0
    x, dx = build_grid(-12.0, 12.0, 3001)
    states = solve(x, potentials.harmonic(omega=omega), k=6)

    n = np.arange(6)
    expected = analytic.qho_energies(n, omega=omega)

    assert np.allclose(states.energies, expected, rtol=1e-3)


def test_eigenstates_are_orthonormal():
    """Numerical eigenstates should be orthonormal under the trapezoid inner product."""
    x, dx = build_grid(-12.0, 12.0, 2001)
    states = solve(x, potentials.harmonic(), k=5)

    overlap = states.states.T @ states.states * dx
    assert np.allclose(overlap, np.eye(len(states)), atol=1e-6)


def test_harmonic_ground_state_is_gaussian():
    """The QHO ground state is exp(-x^2/2) (up to normalization) for omega=m=1."""
    x, dx = build_grid(-10.0, 10.0, 2001)
    states = solve(x, potentials.harmonic(omega=1.0), k=1)

    psi0 = states.states[:, 0]
    gaussian = np.exp(-(x**2) / 2.0)
    gaussian /= np.sqrt(np.sum(gaussian**2) * dx)

    # Compare densities to be insensitive to an overall sign.
    assert np.allclose(np.abs(psi0) ** 2, gaussian**2, atol=1e-4)


def test_double_well_ground_doublet_is_nearly_degenerate():
    """A deep double well has a closely spaced symmetric/antisymmetric pair."""
    x, dx = build_grid(-4.0, 4.0, 2001)
    states = solve(x, potentials.double_well(a=1.0, b=8.0), k=4)

    splitting = states.energies[1] - states.energies[0]
    gap_to_next = states.energies[2] - states.energies[1]
    # The tunneling splitting is much smaller than the gap to the next level.
    assert splitting < 0.1 * gap_to_next


def test_k_must_be_smaller_than_grid():
    x, _ = build_grid(0.0, 1.0, 10)
    with pytest.raises(ValueError):
        solve(x, potentials.free(), k=10)
