"""Solve a few standard potentials and compare with the analytic spectra.

Run from the project root::

    python examples/eigenstates_demo.py

Writes figures to ``figures/`` and prints validation tables to stdout.
"""

import os
import sys

# Make the package importable when run as "python examples/eigenstates_demo.py".
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

import numpy as np  # noqa: E402

from schrodinger import analytic, build_grid, potentials, solve  # noqa: E402
from schrodinger.plotting import plot_eigenstates, plt  # noqa: E402

FIG_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def _table(title, n, numeric, exact):
    print(f"\n{title}")
    print(f"{'n':>3} {'numerical':>14} {'analytic':>14} {'rel. error':>12}")
    for ni, num, ex in zip(n, numeric, exact):
        rel = abs(num - ex) / abs(ex)
        print(f"{ni:>3} {num:>14.6f} {ex:>14.6f} {rel:>12.2e}")


def infinite_square_well():
    x, _ = build_grid(0.0, 1.0, 1999)
    states = solve(x, potentials.free(), k=5)
    L = states.effective_box_width()
    n = np.arange(1, 6)
    _table("Infinite square well (E_n = n^2 pi^2 / 2L^2)", n, states.energies, analytic.isw_energies(n, L))


def harmonic_oscillator():
    x, _ = build_grid(-12.0, 12.0, 3001)
    states = solve(x, potentials.harmonic(omega=1.0), k=6)
    n = np.arange(6)
    _table("Harmonic oscillator (E_n = n + 1/2)", n, states.energies, analytic.qho_energies(n))

    V = potentials.harmonic(omega=1.0)
    fig, _ = plot_eigenstates(states, V, n_states=6, scale=0.7, title="Harmonic oscillator eigenstates")
    fig.savefig(os.path.join(FIG_DIR, "harmonic_eigenstates.png"), dpi=130)
    plt.close(fig)


def double_well():
    x, _ = build_grid(-4.0, 4.0, 2001)
    V = potentials.double_well(a=1.0, b=8.0)
    states = solve(x, V, k=6)
    print("\nQuartic double well V(x) = x^4 - 8x^2  (lowest 6 energies)")
    print(states.energies)
    print(f"ground-state tunneling splitting E1 - E0 = {states.energies[1] - states.energies[0]:.3e}")

    fig, _ = plot_eigenstates(states, V, n_states=6, scale=0.4, title="Double-well eigenstates")
    fig.savefig(os.path.join(FIG_DIR, "double_well.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    infinite_square_well()
    harmonic_oscillator()
    double_well()
    print(f"\nFigures written to {os.path.normpath(FIG_DIR)}/")
