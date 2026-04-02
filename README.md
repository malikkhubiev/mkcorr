[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19163753.svg)](https://doi.org/10.5281/zenodo.19163753)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# MK Directional Consistency Measure & DCI Framework

## What This Is

A diagnostic framework for detecting inconsistency, hidden heterogeneity, and structural breaks in sequential data. The framework combines two measures:

- **Spearman's ρ** — global monotonic direction
- **MK (Directional Consistency Measure)** — local stepwise consistency

The core contribution is not a new correlation coefficient but a **dual-metric interpretation framework (DCI)** where disagreement between measures signals latent data problems.

## Definition

For sequence y₁,...,yₙ sorted by x if x is not provided, observations are assumed ordered in time or sequence:

**Step 1 — Successive differences:**
δᵢ = sign(yᵢ - yᵢ₋₁) ∈ {-1, 0, +1}

**Step 2 — Global trend:**
M = sign(∑δᵢ)
where sign(0) = 0

**Step 3 — Counts:**
P = #{δᵢ = +1}, N = #{δᵢ = -1}

**Step 4 — MK:**
- If M = +1: MK = (P + 1)/n
- If M = -1: MK = -(N + 1)/n  
- If M = 0: MK = (P - N)/n

+1 accounts for the first observation aligned with global trend direction

**Properties:**
- Range: [-1, 1]
- Not symmetric (x defines ordering)
- Depends on sequence order (by design)
- O(n) complexity after sorting
- Single outlier changes MK by at most 1/n

## Diagnostic Matrix (DCI)

| ρ | MK | Diagnosis | Business Implication |
|---|---|---|---|
| >0 | >0 | Consistent trend | Trust the signal |
| >0 | <0 | Trend with reversals | Increase horizon, don't trade short-term |
| <0 | <0 | Consistent decline | Exit / retrain |
| <0 | >0 | Decline with bounces | Bull trap — avoid false signals |
| ≈0 | >0 | Local structure, no global | Segment data — effect cancels |
| ≈0 | <0 | Pure noise | Measurement problem |

**Core diagnostic rule:** Sign disagreement between ρ and MK is a strong diagnostic signal and practical warning of latent heterogeneity or structural breaks.

## Why Not Kendall's τ?

Kendall's τ (pairwise) and MK (sequential) answer different questions:

| | Kendall's τ | MK |
|---|---|---|
| Comparison type | All pairs (n²/2) | Adjacent only (n-1) |
| Complexity | O(n log n) optimized | O(n) |
| Sensitive to | Global concordance | Stepwise consistency |
| Order matters? | No (invariant to permutation) | Yes (by design) |

Use MK when order and stepwise behavior matter. Use Kendall's τ when you need permutation-invariant association.

## Application Areas

### Finance

**Portfolio construction:** Filter by MK. Assets with MK > 0.6 exhibit consistent trends suitable for trend-following. Assets with ρ > 0 but MK < 0 produce gains through rare large moves while losing on most steps — unsuitable for short-term strategies.

**Strategy validation:** A backtest showing ρ > 0 but MK < 0 indicates the strategy profits from infrequent events. Not reliable for execution without understanding these events.

**Risk management:** When ρ and MK diverge, increase holding horizon. Local losses are compensated by global trend.

### ML Model Evaluation

**Stability monitoring:** High ρ with low MK indicates model correct on average but inconsistent stepwise. Signals overfitting or concept drift before global metrics degrade.

**LLM reasoning assessment:** ρ measures answer correctness. MK measures reasoning step consistency. High ρ with low MK means correct answers via flawed reasoning — unacceptable for production.

### Ranking Systems (Search, RecSys)

**User trust:** Low MK with acceptable ρ produces "correct on average but jumps erratically" experience. Users cannot form mental model of system behavior.

**A/B testing diagnosis:** ρ unchanged but MK changed significantly indicates treatment effects exist but cancel globally. Requires segment analysis.

### DevOps / System Monitoring

**Anomaly detection:** MK < 0.3 indicates metric behaves as noise. Alert thresholds on such metrics generate false positives.

**Incident validation:** During incident, negative MK confirms consistent degradation. Positive MK with negative ρ suggests intermittent issues — different root cause.

### A/B Testing

**Heterogeneous effects:** |ρ| < ε where ε is a small threshold (e.g., 0.05) but MK ≠ 0 → treatment affects subgroups differently. Do not conclude "no effect" without segmentation.

**Guardrail metrics:** High MK indicates reliable monitoring metric. Low MK means metric oscillates — use with caution.

### Scientific Data Analysis

**Simpson's paradox detection:** Sign disagreement between ρ and MK is a practical indicator of potential Simpson's paradox or hidden heterogeneity. Triggers stratified analysis.

**Experimental design:** Low MK in control group indicates measurement noise exceeds signal. Increase sample size or improve measurement.

## When to Use Which

| Question | Method |
|----------|--------|
| Global trend direction? | Spearman's ρ |
| Data has outliers? | MK |
| Need O(n) on millions of points? | MK |
| Detect heterogeneity/structural breaks? | DCI (ρ + MK) |
| Stepwise consistency matters? | MK |
| Compare with published results? | Spearman's ρ |
| Permutation-invariant association? | Kendall's τ |

## Interpretation

- MK ≈ 1 → nearly all steps follow a consistent upward trend  
- MK ≈ -1 → nearly all steps follow a consistent downward trend  
- MK ≈ 0 → no consistent local direction (oscillating or noisy behavior)

`MK can be interpreted as an empirical estimate of the probability that the next step follows the global trend direction.`

## Limitations

- MK ignores magnitude (small and large changes count equally)
- Standard version conservative with ties (ties-corrected version available)
- Discontinuity at trend direction flip (magnitude 1/n, negligible for n large)
- Not symmetric in x and y (by design — x defines ordering)
- Not a correlation coefficient in mathematical statistics sense (not centered, permutation-variant)

## Installation

```bash
pip install git+https://github.com/malikkhubiev/mkcorr.git
```

## Quick Example

```python
import numpy as np
from mkcorr import mk_coefficient
from scipy.stats import spearmanr

# Data: increasing with one outlier
y = [1, 2, 3, 100, 4, 5, 6, 7]

rho, _ = spearmanr(y)  # 0.95 — global positive
mk = mk_coefficient(y)  # 0.75 — slightly reduced by outlier

# DCI diagnosis: consistent trend (both positive)
```

## Citation

```bibtex
@software{khubiev2026mk,
  author = {Khubiev, Malik},
  title = {MK Directional Consistency Measure and DCI Framework},
  year = {2026},
  doi = {10.5281/zenodo.19163753}
}
```

## License

MIT License - feel free to use, modify, and distribute with attribution.

## Links

- **Zenodo:** [https://doi.org/10.5281/zenodo.19163753](https://doi.org/10.5281/zenodo.19163753)
- **GitHub:** [https://github.com/malikkhubiev/mkcorr](https://github.com/malikkhubiev/mkcorr)

## Contact

Malik Khubiev - [malik.hubiev@mail.ru](mailto:malik.hubiev@mail.ru)
