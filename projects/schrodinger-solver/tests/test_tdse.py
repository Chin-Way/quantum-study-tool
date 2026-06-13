"""The time-dependent solver is checked for the things it must get right:
unitarity, free-particle motion, energy conservation, and tunneling."""

import numpy as np

from schrodinger import SplitStepSolver, analytic, build_grid, gaussian_wavepacket, potentials


def test_norm_is_conserved():
    """Split-step is unitary: the norm must stay 1 to machine precision."""
    x, _ = build_grid(-50.0, 50.0, 4096)
    solver = SplitStepSolver(x, potentials.free())
    psi = gaussian_wavepacket(x, x0=-10.0, k0=3.0, sigma=2.0)

    _, frames = solver.evolve(psi, dt=0.005, steps=400, save_every=50)
    norms = [solver.norm(f) for f in frames]
    assert np.allclose(norms, 1.0, atol=1e-10)


def test_free_particle_moves_at_group_velocity():
    """For a free packet <x>(t) = x0 + (hbar k0 / m) t."""
    x, _ = build_grid(-50.0, 50.0, 4096)
    solver = SplitStepSolver(x, potentials.free())
    x0, k0 = -10.0, 4.0
    psi = gaussian_wavepacket(x, x0=x0, k0=k0, sigma=2.0)

    dt, steps = 0.005, 1000
    _, frames = solver.evolve(psi, dt=dt, steps=steps, save_every=steps)
    t = dt * steps
    expected = x0 + (solver.hbar * k0 / solver.m) * t
    assert abs(solver.expectation_x(frames[-1]) - expected) < 0.05


def test_energy_is_conserved():
    """A static potential conserves <H>."""
    x, _ = build_grid(-50.0, 50.0, 4096)
    solver = SplitStepSolver(x, potentials.harmonic(omega=0.3))
    psi = gaussian_wavepacket(x, x0=-5.0, k0=0.0, sigma=1.5)

    e0 = solver.energy(psi)
    _, frames = solver.evolve(psi, dt=0.002, steps=2000, save_every=2000)
    e1 = solver.energy(frames[-1])
    assert abs(e1 - e0) / abs(e0) < 1e-3


def test_tunneling_matches_analytic_order_of_magnitude():
    """A wavepacket hitting a barrier transmits roughly as the plane-wave T(E_0).

    The packet has an energy spread, so we only require the same order of
    magnitude as the analytic transmission at the mean energy -- enough to
    catch a wrong physical result while tolerating the finite bandwidth.
    """
    x, _ = build_grid(-60.0, 60.0, 8192)
    V0, width = 3.0, 1.0
    solver = SplitStepSolver(x, potentials.barrier(height=V0, width=width, x0=0.0))

    k0 = 2.0  # mean energy E0 = k0^2 / 2 = 2.0 < V0 -> tunneling
    psi = gaussian_wavepacket(x, x0=-20.0, k0=k0, sigma=3.0)
    E0 = 0.5 * k0**2

    _, frames = solver.evolve(psi, dt=0.004, steps=3000, save_every=3000)
    T_num = solver.transmitted_probability(frames[-1], x_split=width)
    T_analytic = analytic.square_barrier_transmission(E0, V0=V0, a=width)

    assert 0.0 < T_num < 1.0
    # within a factor of ~4 of the plane-wave estimate
    assert 0.25 < T_num / T_analytic < 4.0
