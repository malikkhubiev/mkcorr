# MK Correlation Coefficient

Malik Khubiev's Correlation Coefficient (MK) - a robust, sign-based measure of monotonic relationship.

## Features
- **O(n) computational complexity** — fast enough for millions of data points
- **Highly resistant to outliers** — single outlier changes MK by at most $$1/n$$
- **Bootstrap confidence intervals** — uncertainty quantification
- **Permutation tests** — hypothesis testing for significance
- **Ties-corrected version** — handles datasets with repeated values
- **Intuitive interpretation** — ranges from $$-1$$ (perfectly decreasing) to $$1$$ (perfectly increasing)

## Installation

```bash
# Install from PyPI (coming soon)
pip install mkcorr

# Or install directly from GitHub
pip install git+https://github.com/malikkhubiev/mkcorr.git
```

## Quick Start

```python
import numpy as np
from mkcorr import mk_coefficient, mk_ties_corrected, mk_ci, mk_test

# Example data with an outlier
y = [1, 2, 3, 100, 4, 5, 6, 7]

# 1. Compute MK coefficient
mk = mk_coefficient(y)
print(f"MK = {mk:.3f}")  # MK = 0.750

# 2. Ties-corrected version (for data with repeated values)
y_ties = [1, 1, 2, 2, 3, 3, 4, 4]
mk_ties = mk_ties_corrected(y_ties)
print(f"MK (ties-corrected) = {mk_ties:.3f}")  # MK = 0.833

# 3. Bootstrap confidence interval
ci_low, ci_high = mk_ci(y, B=1000)
print(f"95% CI: [{ci_low:.3f}, {ci_high:.3f}]")

# 4. Permutation test for significance
mk_obs, p_value = mk_test(y)
print(f"p-value = {p_value:.3f}")
```

## Detailed Usage

### Basic MK Coefficient

```python
from mkcorr import mk_coefficient

# Strictly increasing sequence
print(mk_coefficient([1, 2, 3, 4]))        # 1.0

# Strictly decreasing sequence
print(mk_coefficient([4, 3, 2, 1]))        # -1.0

# Sequence with an outlier (the motivating example)
print(mk_coefficient([2, 3, 1, 4]))        # 0.75

# Sequence with no clear trend
print(mk_coefficient([1, 2, 1, 2, 1]))     # 0.0
```

### Ties-Corrected Version

When your data contains many repeated consecutive values, the standard MK coefficient is conservative. Use the ties-corrected version:

```python
from mkcorr import mk_coefficient, mk_ties_corrected

y = [1, 1, 2, 2, 3, 3, 4, 4]

print(f"Standard MK: {mk_coefficient(y):.3f}")        # 0.625
print(f"Ties-corrected MK: {mk_ties_corrected(y):.3f}")  # 0.833
```

### Bootstrap Confidence Intervals

```python
from mkcorr import mk_ci

y = [1, 2, 3, 100, 4, 5, 6, 7]

# 95% confidence interval
ci_95 = mk_ci(y, B=1000, alpha=0.05)
print(f"95% CI: [{ci_95[0]:.3f}, {ci_95[1]:.3f}]")

# 90% confidence interval
ci_90 = mk_ci(y, B=1000, alpha=0.10)
print(f"90% CI: [{ci_90[0]:.3f}, {ci_90[1]:.3f}]")
```

### Permutation Test

```python
from mkcorr import mk_test

y = [1, 2, 3, 100, 4, 5, 6, 7]
mk_obs, p_value = mk_test(y, B=10000)
print(f"Observed MK = {mk_obs:.3f}")
print(f"P-value = {p_value:.4f}")

if p_value < 0.05:
    print("Significant trend detected (p < 0.05)")
```

### Working with (x, y) Pairs

If your data comes as (x, y) pairs, sort by x first:

```python
import numpy as np
from mkcorr import mk_coefficient, mk_test

# Unsorted data
x = [10, 20, 5, 15, 25]
y = [2, 4, 1, 3, 5]

# Sort by x
idx = np.argsort(x)
y_sorted = np.array(y)[idx]

# Now compute MK
mk = mk_coefficient(y_sorted)
print(f"MK = {mk:.3f}")

# Permutation test with x
mk_obs, p_value = mk_test(y, x=x)  # pass x for proper ordering
print(f"p-value = {p_value:.4f}")
```

## Properties

- **Range:** $$\text{MK} \in [-1, 1]$$
- **Complexity:** $$O(n)$$ after sorting
- **Robustness:** Single outlier changes MK by at most $$1/n$$
- **Breakdown point:** $$0.5$$ (can tolerate up to 50% contamination)
- **Invariance:** Preserved under any order-preserving transformation of $$y$$
- **Ties:** Naturally handled; ties-corrected version available
- **Asymptotic normality:** Under independence, $$\sqrt{n}\,\text{MK} \xrightarrow{d} N(0,1)$$

## Citation

If you use MK correlation in your research, please cite:

```bibtex
@article{khubiev2026mk,
  title={Malik Khubiev's Correlation Coefficient: A Robust Sign-Based Measure of Monotonic Relationship},
  author={Khubiev, Malik},
  journal={arXiv preprint},
  year={2026}
}
```

## License

MIT License - feel free to use, modify, and distribute with attribution.

## Links

- **GitHub:** [https://github.com/malikkhubiev/mkcorr](https://github.com/malikkhubiev/mkcorr)
- **arXiv:** (coming soon)
- **PyPI:** (coming soon)

## Contact

Malik Khubiev - [malik.hubiev@mail.ru](mailto:malik.hubiev@mail.ru)
