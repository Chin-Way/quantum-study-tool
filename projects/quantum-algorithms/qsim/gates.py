"""Standard quantum gates as NumPy matrices.

Single-qubit gates are 2x2; two-qubit gates are 4x4 in the basis ordered
|q0 q1> with q0 the most-significant bit (00, 01, 10, 11). Everything here is
unitary, which the test-suite checks explicitly.
"""

from __future__ import annotations

import numpy as np

_SQRT2 = np.sqrt(2.0)

# --- single-qubit gates --------------------------------------------------

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / _SQRT2
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)


def phase(theta: float) -> np.ndarray:
    """Phase gate diag(1, e^{i theta})."""
    return np.array([[1, 0], [0, np.exp(1j * theta)]], dtype=complex)


def rx(theta: float) -> np.ndarray:
    """Rotation about x by angle theta."""
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)


def ry(theta: float) -> np.ndarray:
    """Rotation about y by angle theta."""
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def rz(theta: float) -> np.ndarray:
    """Rotation about z by angle theta."""
    return np.array([[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]], dtype=complex)


# --- two-qubit gates (control = q0, target = q1) -------------------------

CNOT = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)

CZ = np.diag([1, 1, 1, -1]).astype(complex)

SWAP = np.array(
    [
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ],
    dtype=complex,
)


def controlled(U: np.ndarray) -> np.ndarray:
    """Build the controlled version of a single-qubit gate ``U`` (control = q0)."""
    U = np.asarray(U, dtype=complex)
    out = np.eye(4, dtype=complex)
    out[2:, 2:] = U
    return out
