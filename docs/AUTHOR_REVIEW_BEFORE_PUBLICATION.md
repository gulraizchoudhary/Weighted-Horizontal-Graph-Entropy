# Author review checklist (not for blind public claims)

This package was assembled from the manuscript(s), supplied original scripts and
supplied aggregate results. Scientific content was not re-estimated.

- [ ] Confirm that the **final chosen scientific implementation** is HVG +
      per-window TotalWeight + 20 equal-width bins, not an exploratory mean/SEM pathway.
- [ ] Compare a few known subject/realization WHVGE and GHVG outputs numerically
      against the trusted frozen analysis, matching preprocessing and parameter settings.
- [ ] Check results/ CSV tables line by line against the current manuscript version;
      remove outdated or redundant tables.
- [ ] Decide whether to release a complete reproduction pipeline (later scripts not
      supplied in this packaged example); update the Data and code availability
      statement to match the actual repository contents.
- [ ] Decide how to treat age/quadratic-age analysis after mentor's Fig. 3C changes;
      avoid public plots that suggest removed results are still in the paper.
- [ ] Confirm code ownership, choose a LICENSE, add a repository URL and final citation.
- [ ] Do not commit patient data, individual-level CSVs, identifiers, mapping tables,
      absolute local machine paths, or unpublished exploratory work without approval.

Known issues in early research scripts:
1. `weight_hvg_entropy.py`: `weight_mean_sem` uses HVG, but
   `total_window_weight` uses VG.
2. `weight_hvg_main.py`: `weight_series` returns per-window mean/SEM/edge count;
   `np.histogram` operates on its matrix, rather than total graph weight.
3. Original histogram uses `np.linspace(min,max,n_bins)`, giving `n_bins-1`
   intervals. This release deliberately uses `np.histogram(..., bins=20)`.

These differences are transparently documented, not hidden or relabeled.
