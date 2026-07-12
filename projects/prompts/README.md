# Project build prompts

Paste-ready prompts for building new scientific-computing portfolio projects. Open a
fresh Claude Code session on a new empty repo, paste the whole file, and let it run.
Each prompt specifies the package layout, physics/math validation targets, a quality
bar, and a commit/push workflow.

## Saved here (batch 2 — fact-checked physics)

| Prompt | Domain | Signature "wow" |
|---|---|---|
| [`molecular-dynamics.md`](molecular-dynamics.md) | statistical physics | Lennard-Jones liquid → g(r), Maxwell–Boltzmann speeds |
| [`percolation.md`](percolation.md) | critical phenomena | union-find clusters, p_c ≈ 0.5927, finite-size scaling |
| [`game-of-life.md`](game-of-life.md) | cellular automata | glider-gun GIF, exact period tests |
| [`fft-spectral.md`](fft-spectral.md) | signal processing | Cooley–Tukey FFT from scratch, spectrograms |
| [`reaction-diffusion.md`](reaction-diffusion.md) | PDEs / pattern formation | Gray–Scott Turing patterns |
| [`autograd-nn.md`](autograd-nn.md) | ML / autodiff | a tiny PyTorch-style autograd + gradient checks |

## Also proposed (batch 1 — prompts delivered in chat)

`orbital-mechanics` (N-body gravity) · `lattice-boltzmann` (vortex street) ·
`rsa-from-scratch` (cryptography) · `chaotic-pendulum` (deterministic chaos) ·
`pagerank` (network science) · `raytracer` (computer graphics).

Plus deepen-them prompts for the three published repos: `schrodinger-solver`
(2-D solver + animation), `quantum-algorithms` (QFT → phase estimation → Shor),
`ml-ising-phases` (CNN vs MLP + finite-size scaling).
