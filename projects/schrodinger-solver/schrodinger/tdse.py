"""Time-dependent Schrödinger equation via the split-step Fourier method.

We propagate

    i hbar d/dt psi = [ -hbar^2/(2m) d^2/dx^2 + V(x) ] psi

with the symmetric (Strang) operator splitting

    psi(t + dt) = e^{-i V dt / 2hbar} . F^{-1} e^{-i hbar k^2 dt / 2m} F . e^{-i V dt / 2hbar} psi(t)

where ``F`` is the FFT. The potential step is diagonal in position space and
the kinetic step is diagonal in momentum space, so each factor is a pure phase:
the scheme is unitary to machine precision and conserves the norm exactly. It
is second-order accurate in ``dt``.

The grid is treated as periodic (that is what the FFT assumes), so keep the
domain wide enough that the wavepacket never wraps around.
"""

from __future__ import annotations

import numpy as np


def gaussian_wavepacket(x: np.ndarray, x0: float, k0: float, sigma: float) -> np.ndarray:
    """A normalized Gaussian wavepacket.

    Centered at ``x0`` in position with mean wavenumber ``k0`` (mean momentum
    ``hbar k0``) and position width ``sigma``.
    """
    psi = np.exp(-((x - x0) ** 2) / (2.0 * sigma**2)) * np.exp(1j * k0 * x)
    dx = x[1] - x[0]
    psi /= np.sqrt(np.sum(np.abs(psi) ** 2) * dx)
    return psi.astype(complex)


class SplitStepSolver:
    """Split-step Fourier propagator for a fixed potential on a uniform grid."""

    def __init__(self, x: np.ndarray, V, hbar: float = 1.0, m: float = 1.0):
        self.x = x
        self.dx = x[1] - x[0]
        self.N = len(x)
        self.hbar = hbar
        self.m = m
        self.V = V(x) if callable(V) else np.asarray(V, dtype=float)
        # Angular wavenumbers matching numpy's FFT ordering.
        self.k = 2.0 * np.pi * np.fft.fftfreq(self.N, d=self.dx)
        self._kinetic_phase_cache: dict[float, np.ndarray] = {}

    def _kinetic_phase(self, dt: float) -> np.ndarray:
        phase = self._kinetic_phase_cache.get(dt)
        if phase is None:
            phase = np.exp(-1j * self.hbar * self.k**2 * dt / (2.0 * self.m))
            self._kinetic_phase_cache[dt] = phase
        return phase

    def step(self, psi: np.ndarray, dt: float) -> np.ndarray:
        """Advance ``psi`` by one time step ``dt`` (Strang splitting)."""
        half_V = np.exp(-1j * self.V * dt / (2.0 * self.hbar))
        psi = half_V * psi
        psi = np.fft.ifft(self._kinetic_phase(dt) * np.fft.fft(psi))
        psi = half_V * psi
        return psi

    def evolve(self, psi0: np.ndarray, dt: float, steps: int, save_every: int = 1):
        """Evolve ``psi0`` for ``steps`` steps, snapshotting every ``save_every``.

        Returns ``(times, frames)`` where ``frames`` has shape ``(n_saved, N)``.
        """
        psi = np.asarray(psi0, dtype=complex).copy()
        frames = [psi.copy()]
        times = [0.0]
        for n in range(1, steps + 1):
            psi = self.step(psi, dt)
            if n % save_every == 0:
                frames.append(psi.copy())
                times.append(n * dt)
        return np.array(times), np.array(frames)

    # --- diagnostics -----------------------------------------------------

    def norm(self, psi: np.ndarray) -> float:
        """Total probability ``integral |psi|^2 dx`` (should stay ~1)."""
        return float(np.sum(np.abs(psi) ** 2) * self.dx)

    def expectation_x(self, psi: np.ndarray) -> float:
        """Position expectation value ``<x>``."""
        return float(np.sum(self.x * np.abs(psi) ** 2) * self.dx)

    def energy(self, psi: np.ndarray) -> float:
        """Expectation value ``<H>`` (kinetic via FFT + potential in place)."""
        psi_k = np.fft.fft(psi)
        kinetic = np.sum((self.hbar**2 * self.k**2 / (2.0 * self.m)) * np.abs(psi_k) ** 2)
        kinetic *= self.dx / self.N  # Parseval normalization for numpy's FFT
        potential = np.sum(self.V * np.abs(psi) ** 2) * self.dx
        return float(kinetic + potential)

    def transmitted_probability(self, psi: np.ndarray, x_split: float) -> float:
        """Probability to the right of ``x_split`` -- transmission past a barrier."""
        mask = self.x > x_split
        return float(np.sum(np.abs(psi[mask]) ** 2) * self.dx)
