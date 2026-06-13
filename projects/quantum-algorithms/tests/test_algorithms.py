"""Grover, teleportation, and Deutsch-Jozsa must do what they claim."""

import numpy as np
import pytest

from qsim import algorithms


@pytest.mark.parametrize("marked", ["101", "000", "111", "010"])
def test_grover_amplifies_marked_state(marked):
    reg, iters = algorithms.grover(n=3, marked=marked, seed=0)
    pd = reg.prob_dict()
    best = max(pd, key=pd.get)
    assert best == marked
    assert pd[marked] > 0.9  # high success probability after optimal iterations


def test_grover_scales_to_more_qubits():
    marked = "10110"
    reg, _ = algorithms.grover(n=5, marked=marked, seed=1)
    assert reg.probabilities().argmax() == int(marked, 2)
    assert reg.prob_dict()[marked] > 0.95


@pytest.mark.parametrize(
    "alpha,beta",
    [(1, 0), (0, 1), (1, 1), (1, 1j), (0.6, 0.8), (0.3, 0.7 + 0.2j)],
)
def test_teleportation_fidelity(alpha, beta):
    norm = np.sqrt(abs(alpha) ** 2 + abs(beta) ** 2)
    target = np.array([alpha, beta], dtype=complex) / norm

    _, _, out = algorithms.teleport(alpha, beta, seed=7)

    # Fidelity |<target|out>|^2 should be ~1 (up to an unobservable global phase).
    fidelity = abs(np.vdot(target, out)) ** 2
    assert fidelity > 1 - 1e-9


def test_deutsch_jozsa_constant():
    assert algorithms.deutsch_jozsa(n=3, oracle="constant", seed=0) == "constant"


def test_deutsch_jozsa_balanced():
    assert algorithms.deutsch_jozsa(n=3, oracle="balanced", seed=0) == "balanced"
