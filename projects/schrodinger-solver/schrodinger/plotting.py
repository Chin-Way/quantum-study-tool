"""Plotting helpers (matplotlib).

Kept separate from the physics so the solver has no hard dependency on a
plotting backend. Uses the non-interactive ``Agg`` backend so the examples run
headless (CI, servers) and write files directly.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless-safe; must precede pyplot import
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from .tise import Eigenstates  # noqa: E402


def plot_eigenstates(states: Eigenstates, V, n_states: int = 5, scale: float = 1.0, title: str = ""):
    """Plot the potential with the lowest wavefunctions drawn at their energies.

    Each ``psi_n`` is offset vertically to its eigenvalue ``E_n`` (the standard
    textbook picture), with ``scale`` controlling the drawn amplitude.
    """
    x = states.x
    Vx = V(x) if callable(V) else np.asarray(V, dtype=float)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, Vx, color="black", lw=1.5, label="V(x)")

    n_states = min(n_states, len(states))
    colors = plt.cm.viridis(np.linspace(0, 0.85, n_states))
    for n in range(n_states):
        E = states.energies[n]
        psi = states.states[:, n]
        ax.axhline(E, color=colors[n], ls=":", lw=0.8, alpha=0.6)
        ax.plot(x, scale * psi + E, color=colors[n], lw=1.6, label=f"n={n}, E={E:.3f}")

    # Focus the view on the populated levels rather than the potential walls.
    e_lo, e_hi = states.energies[0], states.energies[n_states - 1]
    span = max(e_hi - e_lo, 1.0)
    ax.set_ylim(min(float(np.min(Vx)), e_lo) - 0.1 * span, e_hi + 0.6 * span)

    ax.set_xlabel("x")
    ax.set_ylabel("energy  /  wavefunction (offset)")
    ax.set_title(title or "Eigenstates (drawn at their energies)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig, ax


def plot_snapshots(x, V, times, frames, x_split=None, title=""):
    """Plot ``|psi(x, t)|^2`` at several times over the potential.

    Good for the README: a single static figure that tells the dynamics story
    (e.g. a wavepacket splitting at a barrier).
    """
    Vx = V(x) if callable(V) else np.asarray(V, dtype=float)
    n = len(times)
    fig, axes = plt.subplots(n, 1, figsize=(8, 1.7 * n), sharex=True)
    axes = np.atleast_1d(axes)

    # Scale the potential to sit nicely behind the densities.
    dens_max = max(float((np.abs(f) ** 2).max()) for f in frames) if n else 1.0
    v_finite = Vx[np.isfinite(Vx)]
    v_scale = dens_max / (np.max(np.abs(v_finite)) + 1e-12) if v_finite.size else 0.0

    for ax, t, psi in zip(axes, times, frames):
        ax.fill_between(x, Vx * v_scale, color="0.85", lw=0)
        ax.plot(x, np.abs(psi) ** 2, color="C0", lw=1.4)
        if x_split is not None:
            ax.axvline(x_split, color="C3", ls="--", lw=0.8)
        ax.set_ylabel(f"t={t:.2f}", fontsize=9)
        ax.set_yticks([])

    axes[-1].set_xlabel("x")
    axes[0].set_title(title or r"$|\psi(x,t)|^2$")
    fig.tight_layout()
    return fig, axes
