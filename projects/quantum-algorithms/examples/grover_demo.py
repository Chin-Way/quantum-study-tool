"""Grover's search: find a marked item in an unstructured database of 2^n
entries with only ~sqrt(2^n) queries.

Run from the project root::

    python examples/grover_demo.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

import numpy as np  # noqa: E402

from qsim import algorithms  # noqa: E402


def main():
    n = 5
    marked = "10110"
    N = 2**n

    reg, iters = algorithms.grover(n=n, marked=marked, seed=0)
    p = reg.prob_dict()[marked]

    print(f"searching {N} = 2^{n} items for |{marked}>")
    print(f"Grover iterations used: {iters}  (classical brute force needs ~{N // 2})")
    print(f"probability of measuring the marked state: {p:.4f}")

    counts = reg.sample(shots=1000)
    top = list(counts.items())[:3]
    print("top measurement outcomes (1000 shots):")
    for bits, c in top:
        print(f"  |{bits}>: {c}")

    # Show the amplification curve as the iterations increase.
    print("\nsuccess probability vs. number of Grover iterations:")
    for k in range(0, 2 * iters + 1, max(1, iters // 4)):
        r, _ = algorithms.grover(n=n, marked=marked, iterations=k, seed=0)
        bar = "#" * int(40 * r.prob_dict().get(marked, 0.0))
        print(f"  {k:2d} | {bar} {r.prob_dict().get(marked, 0.0):.3f}")


if __name__ == "__main__":
    main()
