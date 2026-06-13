"""Time-independent Schrödinger equation via finite differences.

We discretize

    H = -hbar^2 / (2 m) d^2/dx^2 + V(x)

on a uniform grid with Dirichlet boundary conditions (``psi = 0`` half a grid
step beyond the first and last samples) and find the lowest-lying eigenpairs
with a sparse symmetric eigensolver.

Boundary-condition note
------------------------
With ``N`` interior samples spaced by ``dx`` the implicit zeros sit at
``x_min - dx`` and ``x_max + dx``. For the infinite square well this means the
*effective* box width is ``L = (N + 1) * dx`` rather than ``x_max - x_min`` --
a small but real detail that the tests account for.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

from .potentials import Potential


@dataclass
class Eigenstates:
    """Result of :func:`solve`.

    Attributes
    ----------
    x : grid points, shape ``(N,)``
    energies : ascending eigenvalues, shape ``(k,)``
    states : columns are wavefunctions, shape ``(N, k)``, normalized so that
        ``sum |psi|^2 dx = 1``
    dx : grid spacing
    """

    x: np.ndarray
    energies: np.ndarray
    states: np.ndarray
    dx: float

    def __len__(self) -> int:
        return len(self.energies)

    def probability_density(self, n: int) -> np.ndarray:
        """``|psi_n(x)|^2`` for the n-th state (n = 0 is the ground state)."""
        return np.abs(self.states[:, n]) ** 2

    def effective_box_width(self) -> float:
        """Effective infinite-square-well width implied by the grid, ``(N+1) dx``."""
        return (len(self.x) + 1) * self.dx


def build_grid(x_min: float, x_max: float, N: int):
    """Return a uniform grid ``x`` of ``N`` points and its spacing ``dx``."""
    x = np.linspace(x_min, x_max, N)
    dx = x[1] - x[0]
    return x, dx


def hamiltonian(x: np.ndarray, V, hbar: float = 1.0, m: float = 1.0) -> sparse.csr_matrix:
    """Build the sparse finite-difference Hamiltonian (Dirichlet BCs).

    ``V`` may be a callable ``V(x)`` or a precomputed array of on-grid values.
    """
    N = len(x)
    dx = x[1] - x[0]
    Vx = V(x) if callable(V) else np.asarray(V, dtype=float)

    # Three-point stencil for -hbar^2/(2m) d^2/dx^2.
    coeff = hbar**2 / (2.0 * m * dx**2)
    main = 2.0 * coeff + Vx
    off = -coeff * np.ones(N - 1)
    H = sparse.diags([off, main, off], offsets=[-1, 0, 1], format="csr")
    return H


def solve(x: np.ndarray, V, k: int = 6, hbar: float = 1.0, m: float = 1.0) -> Eigenstates:
    """Find the ``k`` lowest eigenstates of ``H`` on grid ``x`` for potential ``V``.

    Returns an :class:`Eigenstates` with energies sorted ascending and
    wavefunctions normalized and sign-fixed (largest lobe positive) so plots
    and tests are reproducible.
    """
    if k >= len(x):
        raise ValueError("k must be smaller than the number of grid points")

    H = hamiltonian(x, V, hbar=hbar, m=m)
    dx = x[1] - x[0]

    # 'SA' = smallest algebraic eigenvalues (the bound-state spectrum).
    energies, vecs = eigsh(H, k=k, which="SA")
    order = np.argsort(energies)
    energies, vecs = energies[order], vecs[:, order]

    # Normalize so that sum |psi|^2 dx = 1.
    norms = np.sqrt(np.sum(np.abs(vecs) ** 2, axis=0) * dx)
    vecs = vecs / norms

    # Deterministic sign convention: largest-magnitude entry is positive.
    for j in range(vecs.shape[1]):
        imax = np.argmax(np.abs(vecs[:, j]))
        if vecs[imax, j] < 0:
            vecs[:, j] *= -1.0

    return Eigenstates(x=x, energies=energies, states=vecs, dx=dx)
