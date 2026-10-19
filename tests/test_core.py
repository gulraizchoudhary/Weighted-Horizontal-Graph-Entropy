import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from whvge import (
    horizontal_visibility_edges, total_graph_weight, binned_shannon_entropy,
    exact_edge_count_entropy, calculate_whvge, WEIGHT_MODES
)

def test_hvg_tie_blocks_visibility():
    e = horizontal_visibility_edges(np.array([2., 2., 2.]))
    assert e.tolist() == [[0, 1], [1, 2]]

def test_hvg_matches_original_definition():
    import networkx as nx
    x = np.array([4., 2., 6., 1., 5., 3., 2., 7.])
    from_original = []
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            if all(x[k] < min(x[i],x[j]) for k in range(i+1,j)):
                from_original.append([i,j])
    assert horizontal_visibility_edges(x).tolist() == from_original

def test_weight_definitions():
    x = np.array([1., 0., 3.])
    e = np.array([[0,2]])
    expected = [2.,2.,1.,4.,4.,np.exp(-1.),np.arctan2(2.,2.)]
    for m, val in zip(WEIGHT_MODES,expected):
        assert total_graph_weight(x,e,m) == pytest.approx(val)

def test_exact_baseline():
    assert exact_edge_count_entropy(np.array([3,3,4,4])) == pytest.approx(1)

def test_histogram():
    assert binned_shannon_entropy(np.array([0.,0.,1.,1.]), bins=2) == pytest.approx(1)
    assert binned_shannon_entropy(np.array([1.,1.,1.]), bins=20) == 0

def test_deterministic_end_to_end():
    x = np.random.default_rng(3).normal(size=240)
    out = calculate_whvge(x, window=100, step=10, bins=20)
    assert len(out) == 8
    assert all(np.isfinite(list(out.values())))
    assert out == calculate_whvge(x, window=100, step=10, bins=20)

def test_reject_bad_input():
    with pytest.raises(ValueError):
        calculate_whvge(np.array([1., np.nan, 2.]),window=2)
    with pytest.raises(ValueError):
        calculate_whvge(np.arange(10.),window=11)
    with pytest.raises(ValueError):
        calculate_whvge(np.arange(100.),window=10,bins=1)
