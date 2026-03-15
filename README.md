# MK Correlation Coefficient

Malik Khubiev's Correlation Coefficient (MK) - a robust, sign-based measure of monotonic relationship.

## Features
- O(n) computational complexity
- Highly resistant to outliers
- Bootstrap confidence intervals
- Permutation tests
- Ties-corrected version

## Installation
```bash
pip install mkcorr
# or
pip install git+https://github.com/malikkhubiev/mkcorr.git
```

## Usage
```python
from mkcorr import mk_coefficient, mk_ci, mk_test

# Example data
y = [1, 2, 3, 100, 4, 5, 6, 7]

# Compute MK coefficient
mk = mk_coefficient(y)
print(f"MK = {mk:.3f}")

# Bootstrap confidence interval
ci_low, ci_high = mk_ci(y, B=1000)
print(f"95% CI: [{ci_low:.3f}, {ci_high:.3f}]")

# Permutation test
p_value = mk_test(y)
print(f"p-value = {p_value:.3f}")
```

## Citation
```bibtex
@article{khubiev2026mk,
  title={Malik Khubiev's Correlation Coefficient: A Robust Sign-Based Measure of Monotonic Relationship},
  author={Khubiev, Malik},
  journal={arXiv preprint},
  year={2026}
}
```

## License
MIT
