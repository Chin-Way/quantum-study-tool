# The Infinite Square Well

The infinite square well is the "hydrogen atom" of introductory quantum
mechanics: simple enough to solve exactly, rich enough to show all the essential
features — quantized energies, stationary states, and orthonormal eigenfunctions.

## The potential

A particle of mass $m$ is confined to the region $0 < x < a$ by the potential

$$
V(x) =
\begin{cases}
0, & 0 < x < a, \\
\infty, & \text{otherwise.}
\end{cases}
$$

Outside the well the particle cannot exist, so $\psi(x) = 0$ there. Inside, the
time-independent Schrödinger equation is

$$
-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} = E\,\psi .
$$

## Solving it

Writing $k = \sqrt{2mE}/\hbar$, this becomes $\psi'' = -k^2\psi$, with general
solution $\psi(x) = A\sin(kx) + B\cos(kx)$.

The wavefunction must be **continuous**, so it has to vanish at the walls:
$\psi(0) = \psi(a) = 0$.

- $\psi(0) = 0 \;\Rightarrow\; B = 0$.
- $\psi(a) = 0 \;\Rightarrow\; A\sin(ka) = 0$, so $ka = n\pi$ for $n = 1, 2, 3, \dots$

That single boundary condition is what **quantizes** the energy.

## The stationary states

Normalizing $\int_0^a |\psi|^2\,dx = 1$ fixes $A = \sqrt{2/a}$, giving

$$
\boxed{\,\psi_n(x) = \sqrt{\frac{2}{a}}\,\sin\!\left(\frac{n\pi x}{a}\right)\,}
\qquad n = 1, 2, 3, \dots
$$

with allowed energies

$$
\boxed{\,E_n = \frac{n^2 \pi^2 \hbar^2}{2 m a^2}\,.}
$$

A few things to notice:

| $n$ | energy | interior nodes |
| --- | ------ | -------------- |
| 1 | $E_1$ | 0 |
| 2 | $4E_1$ | 1 |
| 3 | $9E_1$ | 2 |

- The energies grow as $n^2$, so the levels spread apart as you climb.
- The **ground state** ($n = 1$) has energy $E_1 = \pi^2\hbar^2 / 2ma^2 > 0$ — a
  confined particle can never be completely at rest, a direct consequence of the
  uncertainty principle.
- The $\psi_n$ are **orthonormal**: $\int_0^a \psi_m^*\,\psi_n\,dx = \delta_{mn}$.

## Why it matters

Any state of the particle can be written as a superposition of these stationary
states,

$$
\Psi(x, 0) = \sum_{n=1}^{\infty} c_n \,\psi_n(x),
\qquad
c_n = \int_0^a \psi_n^*(x)\,\Psi(x, 0)\,dx ,
$$

and each term then [evolves in time](#/topic/postulates) by a phase
$e^{-i E_n t / \hbar}$. This "expand, then let each piece rotate" strategy is the
workhorse of the whole subject — you will meet it again in the
[harmonic oscillator](#/topic/harmonic-oscillator).
