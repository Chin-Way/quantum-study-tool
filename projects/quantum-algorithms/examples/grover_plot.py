"""Plot Grover's success probability vs. iteration count (needs matplotlib).

Run from the project root::

    python examples/grover_plot.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from qsim import algorithms  # noqa: E402

FIG_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def main():
    n, marked = 5, "10110"
    N = 2**n
    optimal = round((np.pi / 4) * np.sqrt(N))
    ks = list(range(0, 2 * optimal + 2))
    probs = [algorithms.grover(n, marked, iterations=k, seed=0)[0].prob_dict().get(marked, 0.0) for k in ks]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(ks, probs, "o-", color="C0")
    ax.axvline(optimal, color="C3", ls="--", lw=1, label=f"optimal ≈ (π/4)√N = {optimal}")
    ax.set_xlabel("Grover iterations")
    ax.set_ylabel(f"P(measure |{marked}⟩)")
    ax.set_title(f"Grover search over N = {N} items")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = os.path.join(FIG_DIR, "grover_amplification.png")
    fig.savefig(out, dpi=130)
    print(f"Figure written to {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
