Create a new, from-scratch, portfolio-quality Python project named `fft-spectral`: a Cooley-Tukey FFT implemented from first principles plus a spectral-analysis toolkit, in Python (NumPy). Implement the transform YOURSELF — validate against numpy.fft in the tests, but never call numpy.fft (or scipy.fft) inside the library core. This is a standalone repo meant to sit alongside sibling projects (schrodinger-solver, quantum-algorithms, ml-ising-phases) and must match their style: a clean source package, MATH-validating pytest tests, figure-saving examples, an honest understated README with an embedded figure, and CI. Work in the current empty repository.

STRUCTURE:
- package `spectral/`: fft.py (radix-2 Cooley-Tukey FFT + inverse, from scratch), windows.py (Hann/Hamming/Blackman), analysis.py (power spectral density, short-time Fourier transform / spectrogram, helpers), plotting.py (headless Agg helpers). __init__.py exposes a clean public API and __version__ = "0.1.0".
- tests/ using pytest, checking the MATH (see below).
- examples/ writing into a figures/ directory at the project root.
- README.md; requirements.txt (numpy>=1.24, scipy>=1.10, matplotlib>=3.7, pytest>=7.0); pyproject.toml (setuptools backend, packages = ["spectral"], pythonpath = ["."], testpaths = ["tests"], requires-python >=3.10); LICENSE (MIT, "Copyright (c) 2026 Wei Chen"); .gitignore; .github/workflows/ci.yml named "tests", on push + pull_request, matrix Python 3.10/3.11/3.12, `pip install -r requirements.txt`, `python -m pytest -q`. Examples run headless as `python examples/<name>.py`.

PRIMARY GOAL — a correct FFT from scratch.
- Implement the radix-2 Cooley-Tukey FFT (recursive is fine; an iterative bit-reversal version is a nice bonus) and its inverse, using the convention X[k] = sum_n x[n] * exp(-2j*pi*k*n/N). The radix-2 core requires N = 2^m; for other lengths, zero-pad to the next power of two (document it) or implement Bluestein's algorithm (stretch).
- VALIDATE the math with pytest (these are precise, near machine precision):
    * my_fft(x) matches numpy.fft.fft(x) to atol <= 1e-9 for random complex vectors of sizes 2, 4, 8, ..., 1024.
    * ifft(fft(x)) == x to atol <= 1e-9 (round trip), with the correct 1/N normalization on the inverse.
    * A pure cosine of integer frequency k0 over N samples concentrates essentially all spectral energy in bins k0 and N-k0 (> 99% of the total), with the peak at the correct bin.
    * Parseval / Plancherel holds in the unnormalized (numpy) convention: sum_n |x[n]|^2 == (1/N) * sum_k |X[k]|^2 to rtol <= 1e-9. State this normalization explicitly in code and README.
    * For real-valued input the spectrum is conjugate-symmetric: X[N-k] == conj(X[k]).

SECONDARY GOAL — spectral analysis + visualization.
- Windowing (Hann, Hamming, Blackman) to reduce spectral leakage; a power spectral density estimator; a short-time Fourier transform / spectrogram.
- examples/spectrogram_demo.py synthesizes a linear chirp (frequency sweeping in time) and/or a multi-tone signal and saves figures/spectrogram.png showing the sweeping ridge. examples/denoise_demo.py adds noise to a clean signal, thresholds small Fourier coefficients, inverse-transforms, and plots before/after into figures/denoise.png, reporting the SNR improvement. examples/leakage_demo.py contrasts a non-integer-period sinusoid with and without windowing.
- Test: a windowed single tone still peaks at the correct frequency; in the spectrogram of a chirp, the peak-frequency bin increases monotonically across time frames.

STRETCH (only after the above is green): Bluestein's algorithm for arbitrary N (validated against numpy.fft for non-power-of-two sizes); a 2-D FFT (validated against numpy.fft.fft2) with an image low-pass/high-pass demo; or sub-bin peak-frequency estimation via quadratic interpolation.

QUALITY BAR: the library FFT never calls numpy.fft/scipy.fft (only tests and examples may, for comparison); vectorize where sensible (the recursion itself is fine); roughly 10-15 precise tests, fast in CI; honest README explaining the DFT, the divide-and-conquer O(N log N) idea, Parseval, and windowing, with an embedded spectrogram figure and the REAL measured numbers. Docstrings throughout; headless Agg plotting.

WORKFLOW: work on a branch (or main if the repo is empty); small logical commits (FFT core + tests; windows; PSD/STFT; examples + figures; README); run `python -m pytest -q` before each commit and only commit when green; run the examples to generate the embedded figures and commit them; do NOT open a pull request unless I ask. End with a short summary and the final test results.
