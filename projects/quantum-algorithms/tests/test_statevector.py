"""The simulator must apply gates correctly and stay normalized."""

import numpy as np

from qsim import Register, gates


def test_initial_state_is_all_zeros():
    reg = Register(3)
    assert reg.prob_dict() == {"000": 1.0}


def test_x_flips_qubit():
    reg = Register(1)
    reg.apply(gates.X, [0])
    assert reg.prob_dict() == {"1": 1.0}


def test_x_on_middle_qubit_of_three():
    reg = Register(3)
    reg.apply(gates.X, [1])
    assert reg.prob_dict() == {"010": 1.0}


def test_hadamard_makes_superposition():
    reg = Register(1)
    reg.apply(gates.H, [0])
    probs = reg.probabilities()
    assert np.allclose(probs, [0.5, 0.5])


def test_bell_state():
    """H on q0 then CNOT(q0, q1) makes (|00> + |11>)/sqrt(2)."""
    reg = Register(2)
    reg.apply(gates.H, [0])
    reg.apply(gates.CNOT, [0, 1])
    pd = reg.prob_dict()
    assert set(pd) == {"00", "11"}
    assert np.isclose(pd["00"], 0.5) and np.isclose(pd["11"], 0.5)


def test_cnot_control_zero_is_identity():
    reg = Register(2)
    reg.apply(gates.X, [1])  # |01>
    reg.apply(gates.CNOT, [0, 1])  # control is 0 -> unchanged
    assert reg.prob_dict() == {"01": 1.0}


def test_norm_preserved_under_random_circuit():
    reg = Register(4, seed=0)
    rng = np.random.default_rng(1)
    for _ in range(50):
        q = int(rng.integers(4))
        reg.apply(gates.ry(float(rng.uniform(0, np.pi))), [q])
        c, t = rng.choice(4, size=2, replace=False)
        reg.apply(gates.CNOT, [int(c), int(t)])
    assert np.isclose(reg.norm(), 1.0)


def test_measurement_collapses_and_is_consistent():
    reg = Register(2)
    reg.apply(gates.H, [0])
    reg.apply(gates.CNOT, [0, 1])  # Bell state: outcomes must be correlated
    m0 = reg.measure(0)
    m1 = reg.measure(1)
    assert m0 == m1
    assert np.isclose(reg.norm(), 1.0)


def test_sampling_statistics():
    reg = Register(1, seed=42)
    reg.apply(gates.H, [0])
    counts = reg.sample(shots=4000)
    assert abs(counts["0"] - counts["1"]) < 400  # ~50/50 within noise
