# Stern–Gerlach and Spin-½

Sakurai opens not with waves but with a single experiment that has no classical
explanation: the **Stern–Gerlach (SG) experiment**. It is the cleanest window into
the core of quantum mechanics — a degree of freedom with just *two* states — and it
forces on us the whole machinery of kets, operators, and incompatible observables.

## The experiment

A beam of neutral silver atoms passes through an inhomogeneous magnetic field
oriented along $\hat{z}$. Each atom carries a magnetic moment $\vec{\mu} \propto
\mathbf{S}$, so the field deflects it by an amount proportional to $S_z$.
Classically $\mu_z$ could take any value in a continuous range and we would see a
smear. Instead the beam splits into **exactly two** spots: $S_z$ is quantized,

$$
S_z = \pm \frac{\hbar}{2}.
$$

Label the two outcomes $|+\rangle$ and $|-\rangle$ ("spin up" and "spin down"
along $\hat{z}$). They form a complete basis for the spin state.

## Sequential measurements

Now chain SG devices. Block the $S_z = -\hbar/2$ beam so only $|+\rangle$ survives,
and send it into a second apparatus oriented along $\hat{x}$. The $|+\rangle$ beam
splits **again**, 50/50, into $S_x = \pm\hbar/2$. Select $|S_x; +\rangle$ and send
it into a *third*, $\hat{z}$-oriented apparatus: the beam splits once more. The
information about $S_z$ we so carefully prepared has been **destroyed** by the
intervening $S_x$ measurement.

This is the heart of the matter: $S_x$ and $S_z$ are **incompatible** — no state
has definite values of both at once, exactly as for the polarization of light along
two different axes.

## States as kets

The two-spot result says the spin lives in a **two-dimensional complex vector
space**. The $\hat{x}$- and $\hat{y}$-spin eigenstates are superpositions of the
$\hat{z}$ basis:

$$
|S_x; \pm\rangle = \frac{1}{\sqrt{2}}\big(|+\rangle \pm |-\rangle\big), \qquad
|S_y; \pm\rangle = \frac{1}{\sqrt{2}}\big(|+\rangle \pm i\,|-\rangle\big).
$$

The 50/50 splits are then just $|\langle + | S_x; +\rangle|^2 = \tfrac{1}{2}$, and
likewise for every mismatched pair of axes.

## Spin operators

Each measurement corresponds to a Hermitian operator. In the
$\{|+\rangle, |-\rangle\}$ basis they are $S_i = \tfrac{\hbar}{2}\sigma_i$ with the
**Pauli matrices**

$$
\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad
\sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad
\sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}.
$$

Their commutators encode the incompatibility,

$$
[S_i, S_j] = i\hbar\,\epsilon_{ijk}\,S_k,
$$

while the anticommutators $\{S_i, S_j\} = \tfrac{\hbar^2}{2}\delta_{ij}$ give
$S_x^2 = S_y^2 = S_z^2 = \tfrac{\hbar^2}{4}$ and hence

$$
\mathbf{S}^2 = S_x^2 + S_y^2 + S_z^2 = \frac{3}{4}\hbar^2 = s(s+1)\hbar^2,
\qquad s = \tfrac{1}{2}.
$$

Because $[S_x, S_z] \neq 0$, no state can be simultaneously sharp in two components
— the formal statement of what the sequential experiment showed.
