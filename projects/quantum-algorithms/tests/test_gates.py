"""Gates must be unitary and satisfy the usual identities."""

import numpy as np
import pytest

from qsim import gates


@pytest.mark.parametrize(
    "U",
    [gates.X, gates.Y, gates.Z, gates.H, gates.S, gates.T, gates.CNOT, gates.CZ, gates.SWAP],
)
def test_gate_is_unitary(U):
    U = np.asarray(U)
    assert np.allclose(U.conj().T @ U, np.eye(U.shape[0]))


def test_pauli_relations():
    assert np.allclose(gates.X @ gates.X, np.eye(2))
    assert np.allclose(gates.H @ gates.H, np.eye(2))
    assert np.allclose(gates.X @ gates.Y, 1j * gates.Z)  # XY = iZ
    assert np.allclose(gates.S @ gates.S, gates.Z)  # S^2 = Z


def test_rotations_are_unitary():
    for theta in [0.3, 1.0, 2.7]:
        for R in (gates.rx, gates.ry, gates.rz):
            U = R(theta)
            assert np.allclose(U.conj().T @ U, np.eye(2))


def test_controlled_builds_cnot():
    assert np.allclose(gates.controlled(gates.X), gates.CNOT)
