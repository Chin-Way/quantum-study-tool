"""qsim -- a tiny exact statevector quantum-circuit simulator (NumPy only).

Build circuits on a :class:`~qsim.statevector.Register`, or call the prebuilt
algorithms in :mod:`qsim.algorithms` (Grover search, quantum teleportation,
Deutsch-Jozsa).
"""

from . import algorithms, gates
from .statevector import Register

__all__ = ["Register", "gates", "algorithms"]
__version__ = "0.1.0"
