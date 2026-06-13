"""A tiny exact statevector simulator.

An ``n``-qubit state is stored as a complex tensor of shape ``(2,) * n`` so a
gate can be applied to any qubit by tensor contraction in O(2^n) time, without
ever materializing the full 2^n x 2^n operator. This is what lets Grover scale
to ~12 qubits on a laptop.

Convention: qubit 0 is the most-significant bit, so the basis state with
``register.state[i, j, k] = 1`` is written ``|i j k>``.
"""

from __future__ import annotations

import numpy as np


class Register:
    """A register of ``n`` qubits initialized to ``|00...0>``."""

    def __init__(self, n: int, seed: int | None = None):
        if n < 1:
            raise ValueError("need at least one qubit")
        self.n = n
        self.state = np.zeros((2,) * n, dtype=complex)
        self.state[(0,) * n] = 1.0
        self.rng = np.random.default_rng(seed)

    # --- gate application ------------------------------------------------

    def apply(self, U: np.ndarray, qubits) -> "Register":
        """Apply a ``2^k x 2^k`` gate ``U`` to the listed ``qubits`` (in order)."""
        qubits = list(qubits)
        k = len(qubits)
        U = np.asarray(U, dtype=complex).reshape([2] * k + [2] * k)
        # Contract U's input legs with the targeted qubit axes...
        self.state = np.tensordot(U, self.state, axes=(list(range(k, 2 * k)), qubits))
        # ...tensordot puts the k output legs up front; move them back into place.
        self.state = np.moveaxis(self.state, list(range(k)), qubits)
        return self

    def phase_flip(self, bitstring: str) -> "Register":
        """Multiply the amplitude of one computational basis state by -1.

        This is the elementary action behind a Grover oracle and the
        ``2|0><0| - I`` reflection inside the diffusion operator.
        """
        idx = tuple(int(b) for b in bitstring)
        self.state[idx] *= -1.0
        return self

    # --- inspection ------------------------------------------------------

    def amplitudes(self) -> np.ndarray:
        """Flat amplitude vector of length 2^n (index = integer value of bits)."""
        return self.state.reshape(-1)

    def probabilities(self) -> np.ndarray:
        """Born-rule probabilities over the 2^n basis states."""
        return np.abs(self.amplitudes()) ** 2

    def prob_dict(self, tol: float = 1e-9) -> dict[str, float]:
        """Map ``bitstring -> probability`` for the non-negligible outcomes."""
        probs = self.probabilities()
        return {
            format(i, f"0{self.n}b"): float(p)
            for i, p in enumerate(probs)
            if p > tol
        }

    def norm(self) -> float:
        return float(np.sum(self.probabilities()))

    # --- measurement -----------------------------------------------------

    def measure(self, q: int) -> int:
        """Projectively measure qubit ``q``, collapsing the state in place."""
        other_axes = tuple(i for i in range(self.n) if i != q)
        marg = np.abs(self.state) ** 2
        p = marg.sum(axis=other_axes)  # [P(q=0), P(q=1)]
        outcome = int(self.rng.random() >= p[0])

        # Project out the inconsistent half and renormalize.
        keep = [slice(None)] * self.n
        keep[q] = 1 - outcome
        self.state[tuple(keep)] = 0.0
        self.state /= np.sqrt(self.norm())
        return outcome

    def measure_all(self) -> str:
        """Sample a full bitstring from |amplitudes|^2 and collapse to it."""
        probs = self.probabilities()
        i = int(self.rng.choice(len(probs), p=probs))
        self.state[...] = 0.0
        self.state.reshape(-1)[i] = 1.0
        return format(i, f"0{self.n}b")

    def sample(self, shots: int = 1024) -> dict[str, int]:
        """Sample measurement outcomes ``shots`` times *without* collapsing."""
        probs = self.probabilities()
        draws = self.rng.choice(len(probs), size=shots, p=probs)
        counts: dict[str, int] = {}
        for i in draws:
            key = format(int(i), f"0{self.n}b")
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: -kv[1]))
