"""Quantum teleportation: move an unknown one-qubit state from Alice (q0) to
Bob (q2) using a shared Bell pair and two classical bits.

Run from the project root::

    python examples/teleportation_demo.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

import numpy as np  # noqa: E402

from qsim import algorithms  # noqa: E402


def main():
    # An arbitrary state to teleport.
    alpha, beta = 0.6, 0.8j
    norm = np.sqrt(abs(alpha) ** 2 + abs(beta) ** 2)
    target = np.array([alpha, beta]) / norm

    print(f"state to teleport:  {target[0]:.3f}|0> + {target[1]:.3f}|1>")
    print("-" * 56)

    # Repeat to show all four Bell-measurement branches occur and each works.
    for trial in range(6):
        m0, m1, out = algorithms.teleport(alpha, beta, seed=trial)
        fidelity = abs(np.vdot(target, out)) ** 2
        print(
            f"trial {trial}: Alice measured ({m0},{m1}) -> "
            f"Bob holds {out[0]:.3f}|0> + {out[1]:.3f}|1>   fidelity={fidelity:.6f}"
        )

    print("-" * 56)
    print("Bob recovers the exact state every time, regardless of which of the")
    print("four classical outcomes Alice sends. No-cloning is respected: Alice's")
    print("original qubit is destroyed by her measurement.")


if __name__ == "__main__":
    main()
