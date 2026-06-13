"""Three canonical quantum algorithms, built on the statevector simulator.

Each function is written to be read: the quantum-circuit steps appear in the
same order you would draw them on paper.
"""

from __future__ import annotations

import numpy as np

from . import gates
from .statevector import Register


# --- Grover's search -----------------------------------------------------

def grover(n: int, marked: str, iterations: int | None = None, seed: int | None = None):
    """Grover search over ``2^n`` items for the ``marked`` bitstring.

    Returns ``(register, iterations)``. With the optimal number of iterations
    ~ (pi/4) sqrt(2^n), the marked state's probability approaches 1.
    """
    if len(marked) != n:
        raise ValueError("marked bitstring length must equal n")

    N = 2**n
    if iterations is None:
        iterations = max(1, round((np.pi / 4) * np.sqrt(N)))

    reg = Register(n, seed=seed)

    # 1. Uniform superposition over all 2^n states.
    for q in range(n):
        reg.apply(gates.H, [q])

    for _ in range(iterations):
        # 2a. Oracle: flip the phase of the marked state.
        reg.phase_flip(marked)

        # 2b. Diffusion: reflect about the uniform superposition,
        #     H^n (2|0><0| - I) H^n.
        for q in range(n):
            reg.apply(gates.H, [q])
        reg.phase_flip("0" * n)
        for q in range(n):
            reg.apply(gates.H, [q])

    return reg, iterations


# --- Quantum teleportation ----------------------------------------------

def teleport(alpha: complex, beta: complex, seed: int | None = None):
    """Teleport the one-qubit state ``alpha|0> + beta|1>`` from q0 to q2.

    Returns ``(m0, m1, teleported_amplitudes)`` where ``m0, m1`` are Alice's
    classical measurement outcomes and ``teleported_amplitudes`` is the final
    1-qubit state recovered on Bob's qubit (q2). Up to numerical noise it equals
    the input ``[alpha, beta]``.
    """
    norm = np.sqrt(abs(alpha) ** 2 + abs(beta) ** 2)
    alpha, beta = alpha / norm, beta / norm

    reg = Register(3, seed=seed)
    # Prepare q0 in the unknown state via a custom 2x2 unitary whose first
    # column is (alpha, beta) -- i.e. it maps |0> -> alpha|0> + beta|1>.
    prep = np.array([[alpha, -np.conj(beta)], [beta, np.conj(alpha)]], dtype=complex)
    reg.apply(prep, [0])

    # Entangle q1, q2 into a Bell pair (|00> + |11>)/sqrt(2).
    reg.apply(gates.H, [1])
    reg.apply(gates.CNOT, [1, 2])

    # Bell-basis measurement on q0, q1.
    reg.apply(gates.CNOT, [0, 1])
    reg.apply(gates.H, [0])
    m0 = reg.measure(0)
    m1 = reg.measure(1)

    # Bob's classically-conditioned corrections.
    if m1 == 1:
        reg.apply(gates.X, [2])
    if m0 == 1:
        reg.apply(gates.Z, [2])

    # Extract q2's reduced state (q0, q1 are now definite).
    teleported = reg.state[m0, m1, :].copy()
    teleported /= np.linalg.norm(teleported)
    return m0, m1, teleported


# --- Deutsch-Jozsa -------------------------------------------------------

def deutsch_jozsa(n: int, oracle: str, seed: int | None = None) -> str:
    """Decide whether an ``n``-bit boolean function is constant or balanced.

    ``oracle`` is ``"constant"`` or ``"balanced"``. The algorithm answers with
    a single query (vs. up to 2^{n-1}+1 classically). Returns ``"constant"`` or
    ``"balanced"``; the result is exact, not probabilistic.
    """
    # Work register: q0..q_{n-1}; ancilla: q_n prepared in |->.
    reg = Register(n + 1, seed=seed)
    reg.apply(gates.X, [n])
    for q in range(n + 1):
        reg.apply(gates.H, [q])

    # Phase oracle U_f: |x>|y> -> |x>|y XOR f(x)>, written here as a phase.
    if oracle == "balanced":
        # f(x) = x_0 (the first input bit) is balanced; phase = (-1)^{x_0 . 1}.
        # Implemented as CNOT from q0 into the ancilla.
        reg.apply(gates.CNOT, [0, n])
    elif oracle == "constant":
        pass  # f(x) = 0: identity (a global phase is unobservable)
    else:
        raise ValueError("oracle must be 'constant' or 'balanced'")

    for q in range(n):
        reg.apply(gates.H, [q])

    # Measure the input register: all-zeros => constant, else balanced.
    bits = "".join(str(reg.measure(q)) for q in range(n))
    return "constant" if bits == "0" * n else "balanced"
