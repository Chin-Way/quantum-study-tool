# Portfolio projects (staging area)

Three standalone scientific-computing projects, built and tested here and ready
to become their own repositories. **See [`PUBLISHING.md`](./PUBLISHING.md) for
the ~5-minute steps to publish each one** under your account.

> These live in a branch of `quantum-study-tool` only because they were created
> by a tool that could write to that single repo. They are independent projects
> and each should end up as its own public repo.

## The projects

| Project | Domain | Highlights | Tests |
|---|---|---|---|
| **[schrodinger-solver](./schrodinger-solver)** | Computational physics | Finite-difference bound states + split-step wavepacket dynamics; matches theory to ~10⁻⁶; tunneling demo. | 10 |
| **[quantum-algorithms](./quantum-algorithms)** | Quantum computing | From-scratch NumPy statevector simulator; Grover, teleportation, Deutsch–Jozsa. | 34 |
| **[ml-ising-phases](./ml-ising-phases)** | Physics + ML | Monte Carlo Ising model; a neural net recovers Tc to within 3% without training near it. | 8 |

All three: clean package layout, `pytest` suites that check *physics* (not just
that the code runs), runnable demos that produce the figures in each README, a
permissive MIT license, and a GitHub Actions CI workflow.

```bash
# run any project's tests:
cd schrodinger-solver && pip install -r requirements.txt && python -m pytest -q
```

## Also here

- **[PROFILE_README.md](./PROFILE_README.md)** — content for your GitHub profile
  page (the `Chin-Way/Chin-Way` repo).
- **[PUBLISHING.md](./PUBLISHING.md)** — how to publish everything.
