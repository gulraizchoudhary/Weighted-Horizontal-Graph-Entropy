# Weighted Horizontal Visibility Graph Entropy (WHVGE)

Python implementation and runnable **synthetic example** for the manuscript
*A Weighted Horizontal Visibility Graph Entropy Framework for Time Series Characterization*
(Gulraiz Iqbal Choudhary and Wenhan Yang).

**Release status:** author-review candidate. Source-informed, manuscript-aligned core algorithm;
**not** a certified exact reproduction of all reported tables, models, or figures.
The original exploratory Python scripts also contained other graph summaries; this repository
deliberately implements the **final manuscript definition** rather than silently combining different variants.

## Quick start

Python 3.10+:

```bash
python -m pip install -r requirements.txt
python examples/quickstart.py
python examples/save_plot.py
```

The example uses reproducible synthetic Gaussian data, not clinical recordings.
The plot is an independent tutorial illustration, **not a manuscript figure**.

## Method

For every overlapping window of a univariate finite time series:

1. Construct a *horizontal* visibility graph (HVG). Nodes `i < j` connect only if every
   intermediate `x[k] < min(x[i],x[j])` (ties block visibility).
2. Assign one of seven weights to each visible edge.
3. Sum the edge weights to obtain **TotalWeight** for that window.
4. Estimate Shannon entropy (bits) from **20 equal-width bins per signal** of the resulting
   window-level TotalWeight sequence. The bins are adaptive **within each recording**.
5. For exact GHVG, compute Shannon entropy from the **discrete, unre-binned HVG edge-count** sequence.

Seven weighting modes: `Amplitude`, `Distance`, `Amp/Dist`, `Amp×Dist`,
`SquaredAmp`, `ExpDistance` (λ = 2), and `Angle`.
Index distance denotes separation in observations, not elapsed seconds.

```python
import numpy as np
from whvge import calculate_whvge

x = np.random.default_rng(42).normal(size=400)
scores = calculate_whvge(x, window=100, step=10, bins=20)
print(scores["Amp/Dist"])
print(scores["GHVG (edge count)"])
```

Manuscript reference settings:

| Dataset | Window | Step | Bins | Signal length |
| --- | ---: | ---: | ---: | --- |
| Synthetic and primary clinical | 100 | 10 | 20 | 30,000 |
| Clinical larger-window sensitivity | 200 | 10 | 20 | 30,000 |
| Healthy resting IBI | 100 | 1 | 20 | 250 available IBI |
| Gait | 100 | 1 | 20 | First 1,000 intervals |

The demonstration favors clarity over performance and may be slow on long recordings
with step 1. **Do not** treat its runtime or synthetic results as validation of manuscript estimates.
Missing values must be handled by the dataset preprocessing pipeline *before* calling
`calculate_whvge`; this function rejects non-finite inputs instead of silently dropping them.

## Results provided for reference

`results/` includes four supplied **aggregate** CSV files (synthetic statistics,
gait repeated-measures statistics, graph-only classification model summaries,
and nested-CV model summaries). They are reference output tables, not outputs regenerated
by the runnable demo, and have not been independently re-derived from the original recordings.
The authors should review these files against the final manuscript before public release.
Some exploratory/alternative analyses and their statistical tests may use different
estimands or comparisons than the final tables.

## Reproducibility scope and provenance

- Core: newly organized implementation checked against manuscript equations and
  the supplied original HVG/weight definitions.
- Earlier supplied scripts: `weight_hvg_entropy.py`, `weight_hvg_main.py`,
  `weight_hvg_noise_entropy.py`, `Grouped_hvg_entropy.py`, plotting scripts.
  These were **reviewed**, not copied into the public distribution.
- The early clinical driver used *mean edge weight, SEM and edge count* (a different
  descriptor pathway); another helper used **natural VG** for a total-weight routine.
  These are **not equivalent** to the manuscript's final **HVG TotalWeight** definition.
- Actual nested-CV training scripts and full signal-level processing scripts from later
  work are not present in this minimal release. Model summary CSVs do not replace them.
- In particular, age-related Fig. 3C revisions in mentor messages are **not** encoded as
  a fixed paper result here. That panel can change without changing the core method.
- No original signal recordings, subject-level features, subject mapping, or clinical
  identifiers are distributed in this package.

The final manuscript promises analysis scripts and processed result tables. **This minimal
repository alone does not fulfill an assertion of complete manuscript reproduction.**
Before public release, the authors should either add verified research analysis scripts
and appropriate processed results or revise the manuscript availability statement to
accurately reflect the deposited materials.

## Testing

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

These tests establish internal consistency and selected source-definition checks,
**not** numerical equivalence of all manuscript cohort results.

## Data and citation

Original clinical and gait data were obtained from the separately maintained
[PhysioNet](https://physionet.org/) databases and remain subject to their respective
access, use, and citation conditions. Healthy resting-IBI data likewise come from
the study sources described in the manuscript. Download original data from those
providers rather than redistributing them here.

If you use the code, cite the corresponding WHVGE article when its final publication
details become available. No DOI or publication URL is invented here.

## License

This work is licensed under a **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You are free to share, copy, modify, and redistribute this material in any medium or format, provided appropriate credit is given to the original authors.
