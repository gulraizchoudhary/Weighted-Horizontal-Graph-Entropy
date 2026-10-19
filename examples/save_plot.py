"""Plot deterministic synthetic method outputs; NOT a manuscript figure."""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from whvge import calculate_whvge

rng = np.random.default_rng(42)
sig = rng.normal(size=400)
result = calculate_whvge(sig, window=100, step=10, bins=20)
names, values = list(result), list(result.values())
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.bar(range(len(values)), values, color="steelblue")
ax.set_xticks(range(len(values)), names, rotation=30, ha="right")
ax.set_ylabel("Shannon entropy (bits)")
ax.set_title("Illustrative synthetic signal — not manuscript results")
fig.tight_layout()
outfile = Path(__file__).resolve().parents[1] / "examples" / "synthetic_example.pdf"
fig.savefig(outfile)
print(f"Saved {outfile}")
