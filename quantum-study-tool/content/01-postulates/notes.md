# The Postulates of Quantum Mechanics

Quantum mechanics rests on a small set of postulates. Everything else — the
infinite square well, the hydrogen atom, scattering theory — follows from
applying these rules to a specific system.

## 1. The state

The state of a system is described by a **wavefunction** $\psi(x, t)$ (more
abstractly, a vector $|\psi\rangle$ in a Hilbert space). All physical information
about the system is contained in $\psi$, which is **normalized**:

$$
\int_{-\infty}^{\infty} |\psi(x, t)|^2 \, dx = 1 .
$$

## 2. Observables

Every measurable quantity (position, momentum, energy, …) corresponds to a
**Hermitian operator** $\hat{Q}$. The two you will use constantly are

$$
\hat{x} = x, \qquad \hat{p} = -i\hbar \frac{\partial}{\partial x} .
$$

## 3. Measurement and the Born rule

A measurement of $\hat{Q}$ returns one of its **eigenvalues** $q_n$, where
$\hat{Q}\,\psi_n = q_n \psi_n$. If the system is in state $\psi$, the probability
of measuring $q_n$ is

$$
P(q_n) = |\langle \psi_n | \psi \rangle|^2 ,
$$

and the **expectation value** of $\hat{Q}$ is

$$
\langle Q \rangle = \int_{-\infty}^{\infty} \psi^* \, \hat{Q} \, \psi \, dx .
$$

## 4. Time evolution

Between measurements, the state evolves by the **time-dependent Schrödinger
equation**:

$$
i\hbar \frac{\partial \psi}{\partial t} = \hat{H}\,\psi,
\qquad
\hat{H} = -\frac{\hbar^2}{2m}\frac{\partial^2}{\partial x^2} + V(x) .
$$

## 5. Collapse

Immediately after a measurement that yields $q_n$, the state **collapses** to the
corresponding eigenstate $\psi_n$. A measurement repeated right away then returns
$q_n$ with certainty.
