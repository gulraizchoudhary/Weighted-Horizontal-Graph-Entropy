"""Small deterministic synthetic demonstration; NOT study results."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from whvge import calculate_whvge

rng = np.random.default_rng(42)
signal = rng.normal(size=400)
result = calculate_whvge(signal, window=100, step=10, bins=20)
print("WHVGE / GHVG synthetic example (not manuscript estimates)")
for key, value in result.items():
    print(f"{key:20s} {value:.5f} bits")
