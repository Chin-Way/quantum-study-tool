Create a new, from-scratch, portfolio-quality Python project named `autograd-nn`: a small neural-network framework built on a reverse-mode automatic-differentiation engine you write yourself, in pure NumPy — no PyTorch, TensorFlow, or JAX. This is a standalone repo meant to sit alongside sibling projects (schrodinger-solver, quantum-algorithms, ml-ising-phases) and must match their style: a clean source package, CORRECTNESS-validating pytest tests, figure-saving examples, an honest understated README with an embedded figure, and CI. Work in the current empty repository.

STRUCTURE:
- package `autonn/`: engine.py (the autodiff Tensor with a computational graph and backward()), functional.py (ReLU/tanh/sigmoid/softmax and losses MSE + numerically stable cross-entropy), nn.py (Linear layer, activations, Sequential/Module), optim.py (SGD and Adam), data.py (tiny dataset helpers), plotting.py (headless Agg helpers). __init__.py exposes a clean public API and __version__ = "0.1.0".
- tests/ using pytest, checking CORRECTNESS (see below).
- examples/ writing into a figures/ directory at the project root.
- README.md; requirements.txt (numpy>=1.24, scikit-learn>=1.2, matplotlib>=3.7, pytest>=7.0); pyproject.toml (setuptools backend, packages = ["autonn"], pythonpath = ["."], testpaths = ["tests"], requires-python >=3.10); LICENSE (MIT, "Copyright (c) 2026 Wei Chen"); .gitignore; .github/workflows/ci.yml named "tests", on push + pull_request, matrix Python 3.10/3.11/3.12, `pip install -r requirements.txt`, `python -m pytest -q`. Examples run headless as `python examples/<name>.py`.

PRIMARY GOAL — a correct autodiff engine (this is the heart of the project).
- Implement reverse-mode automatic differentiation: a value/tensor type that records operations on a DAG and, on .backward(), propagates gradients via the chain rule in reverse topological order. Support at least: add, subtract, multiply, matmul, power, exp, log, sum/mean, and the activations ReLU, tanh, sigmoid, plus softmax and the losses MSE and (numerically stable) softmax cross-entropy.
- VALIDATE with a GRADIENT CHECK: for each operation and for a small composed network, the analytic gradient from backward() matches a central finite-difference numerical gradient, (f(x+eps) - f(x-eps)) / (2*eps), to relative tolerance <= 1e-5. Use fixed seeds.
- Also test: a single Linear layer + MSE has gradients matching a hand-derived closed form; softmax outputs are non-negative and sum to 1, and cross-entropy of a confident correct prediction is near 0; a value REUSED in the graph (used twice) correctly ACCUMULATES gradient from both paths (a classic autodiff bug if topological order or += is wrong).

SECONDARY GOAL — it actually learns.
- Build small MLPs with the framework and train with SGD/Adam and mini-batches.
- VALIDATE learning with concrete, seeded targets:
    * XOR: a 2-layer MLP with a nonlinearity learns XOR to 100% accuracy (all 4 patterns), whereas a linear model with no hidden layer CANNOT exceed 75% — assert both. This is the classic demonstration that depth/nonlinearity matters.
    * A standard small dataset: on scikit-learn's load_digits (8x8 images, 10 classes) a small MLP reaches > 90% test accuracy on a held-out split; and/or on make_moons the classifier reaches > 95%.
    * Training loss decreases: final loss is clearly below initial loss.
- examples/decision_boundary.py trains on make_moons and animates/plots the decision boundary evolving over epochs into figures/decision_boundary.png (or .gif). examples/digits_demo.py trains on load_digits and saves a loss/accuracy curve figures/training_curves.png plus a few example predictions.

STRETCH (only after the above is green): dropout and/or a simple Conv2d layer, each with its own gradient check; momentum / weight-decay variants; or a check of your Adam update against a hand-computed reference step on a toy problem.

QUALITY BAR: the engine is pure NumPy and must NOT import any deep-learning library; scikit-learn is used ONLY for datasets and an optional baseline. Every operation is gradient-checked. Roughly 12-18 tests, all fast in CI (tiny nets / few epochs in tests). Honest README explaining reverse-mode autodiff, the chain rule over the graph, and the XOR/nonlinearity story, with an embedded decision-boundary figure and the REAL measured accuracies. Docstrings throughout; seed all randomness; headless Agg plotting.

WORKFLOW: work on a branch (or main if the repo is empty); small logical commits (engine + gradient-check tests; layers/losses; optimizers; XOR; datasets + training; examples + figures; README); run `python -m pytest -q` before each commit and only commit when green; run the examples to generate the embedded figures and commit them; do NOT open a pull request unless I ask. End with a short summary and the final test results.
