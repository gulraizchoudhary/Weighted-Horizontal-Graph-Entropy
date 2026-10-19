"""Reference-style educational implementation of weighted grouped-HVG entropy.

This code implements the mathematical definitions described in the WHVGE
manuscript; it is not asserted to be the authors' original analysis software.
"""
from __future__ import annotations

import numpy as np

WEIGHT_MODES = (
    "Amplitude", "Distance", "Amp/Dist", "Amp×Dist",
    "SquaredAmp", "ExpDistance", "Angle",
)


def horizontal_visibility_edges(x: np.ndarray) -> np.ndarray:
    """Return undirected edge indices (i,j) with i<j.

    An edge exists when every intervening sample is strictly below BOTH
    endpoints. Ties in intervening samples block visibility.
    Readable O(L²) implementation, suitable for small demonstration data.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or not np.all(np.isfinite(x)):
        raise ValueError("x must be a finite, one-dimensional signal")
    edges: list[tuple[int, int]] = []
    for i in range(len(x) - 1):
        highest_between = -np.inf
        for j in range(i + 1, len(x)):
            if j > i + 1:
                highest_between = max(highest_between, x[j - 1])
            if highest_between < min(x[i], x[j]):
                edges.append((i, j))
    return np.asarray(edges, dtype=int).reshape(-1, 2)


def total_graph_weight(x: np.ndarray, edges: np.ndarray, mode: str,
                       decay: float = 2.0) -> float:
    """Sum edge weights for one HVG window, using sample-index distances."""
    if mode not in WEIGHT_MODES:
        raise ValueError(f"Unknown weighting mode: {mode}")
    if not np.isfinite(decay) or decay <= 0:
        raise ValueError("decay must be finite and positive")
    x = np.asarray(x, dtype=float)
    edges = np.asarray(edges, dtype=int).reshape(-1, 2)
    if edges.size == 0:
        return 0.0
    i, j = edges.T
    d = (j - i).astype(float)
    difference = x[j] - x[i]
    amplitude = np.abs(difference)
    if mode == "Amplitude":
        weights = amplitude
    elif mode == "Distance":
        weights = d
    elif mode == "Amp/Dist":
        weights = amplitude / d
    elif mode == "Amp×Dist":
        weights = amplitude * d
    elif mode == "SquaredAmp":
        weights = difference ** 2
    elif mode == "ExpDistance":
        weights = np.exp(-d / decay)
    else:  # Angle: atan2 gives the same magnitude as atan(difference / d) for d>0
        weights = np.abs(np.arctan2(difference, d))
    return float(weights.sum())


def binned_shannon_entropy(values: np.ndarray, bins: int = 20) -> float:
    """Shannon entropy in bits, using equal-width bins per input recording."""
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or not len(values) or not np.all(np.isfinite(values)):
        raise ValueError("values must be a nonempty finite 1D sequence")
    if isinstance(bins, (bool, np.bool_)) or not isinstance(bins, (int, np.integer)) or bins < 2:
        raise ValueError("bins must be an integer >= 2")
    if np.ptp(values) == 0:
        return 0.0
    counts, _ = np.histogram(values, bins=bins)
    p = counts[counts != 0] / counts.sum()
    return float(-np.sum(p * np.log2(p)))


def exact_edge_count_entropy(counts: np.ndarray) -> float:
    """Unweighted grouped HVG baseline: exact edge counts as discrete states."""
    counts = np.asarray(counts)
    if counts.ndim != 1 or not len(counts):
        raise ValueError("counts must be a nonempty 1D sequence")
    _, frequencies = np.unique(counts, return_counts=True)
    p = frequencies / frequencies.sum()
    return float(-np.sum(p * np.log2(p)))


def calculate_whvge(signal: np.ndarray, window: int = 100, step: int = 10,
                    bins: int = 20, decay: float = 2.0) -> dict[str, float]:
    """Return seven weighted entropy measures plus unweighted GHVG entropy.

    Note: positive amplitude scaling, missing-data handling, and all dataset
    preprocessing choices must be specified by the researcher. This function
    accepts complete finite signals only and does not silently preprocess.
    """
    signal = np.asarray(signal, dtype=float)
    if signal.ndim != 1 or not np.all(np.isfinite(signal)):
        raise ValueError("signal must be a finite, one-dimensional array")
    for name, value, minimum in (("window", window, 2), ("step", step, 1), ("bins", bins, 2)):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
            raise ValueError(f"{name} must be an integer >= {minimum}")
    if len(signal) < window:
        raise ValueError("signal is shorter than window")
    if not np.isfinite(decay) or decay <= 0:
        raise ValueError("decay must be finite and positive")
    descriptors = {name: [] for name in WEIGHT_MODES}
    edge_counts = []
    for start in range(0, len(signal) - window + 1, step):
        x = signal[start:start + window]
        edges = horizontal_visibility_edges(x)
        edge_counts.append(len(edges))
        for name in WEIGHT_MODES:
            descriptors[name].append(total_graph_weight(x, edges, name, decay))
    result = {name: binned_shannon_entropy(np.asarray(descriptors[name]), bins)
              for name in WEIGHT_MODES}
    result["GHVG (edge count)"] = exact_edge_count_entropy(np.asarray(edge_counts))
    return result
