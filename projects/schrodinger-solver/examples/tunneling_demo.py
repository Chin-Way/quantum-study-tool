"""Quantum tunneling: send a Gaussian wavepacket at a barrier and measure
how much gets through, then compare with the plane-wave transmission T(E).

Run from the project root::

    python examples/tunneling_demo.py
"""

import os
import sys

# Make the package importable when run as "python examples/tunneling_demo.py".
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

import numpy as np  # noqa: E402

from schrodinger import SplitStepSolver, analytic, build_grid, gaussian_wavepacket, potentials  # noqa: E402
from schrodinger.plotting import plot_snapshots, plt  # noqa: E402

FIG_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def main():
    x, _ = build_grid(-60.0, 60.0, 8192)
    V0, width = 3.0, 1.0
    V = potentials.barrier(height=V0, width=width, x0=0.0)
    solver = SplitStepSolver(x, V)

    k0 = 2.0
    E0 = 0.5 * k0**2  # mean energy, below the barrier -> tunneling
    psi = gaussian_wavepacket(x, x0=-20.0, k0=k0, sigma=3.0)

    dt, steps = 0.004, 3000
    times, frames = solver.evolve(psi, dt=dt, steps=steps, save_every=steps // 4)

    T_num = solver.transmitted_probability(frames[-1], x_split=width)
    T_pw = analytic.square_barrier_transmission(E0, V0=V0, a=width)

    print(f"barrier height V0 = {V0}, width a = {width}")
    print(f"mean energy E0 = {E0:.3f}  (E0/V0 = {E0 / V0:.2f}, tunneling regime)")
    print(f"transmitted probability (wavepacket): {T_num:.4f}")
    print(f"plane-wave transmission T(E0):         {T_pw:.4f}")
    print(f"norm conserved: {solver.norm(frames[-1]):.10f}")

    fig, _ = plot_snapshots(x, V, times, frames, x_split=width, title=r"Wavepacket tunneling: $|\psi(x,t)|^2$")
    out = os.path.join(FIG_DIR, "tunneling.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print(f"\nFigure written to {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
