import numpy as np

def mk_coefficient(y):
    """Compute MK correlation coefficient"""
    y = np.asarray(y)
    n = len(y)
    if n < 2:
        return 0.0
    
    diffs = np.sign(np.diff(y))
    P = np.sum(diffs > 0)
    N = np.sum(diffs < 0)
    S = np.sum(diffs)
    M = np.sign(S)
    
    if M > 0:
        return (P + 1) / n
    elif M < 0:
        return -(N + 1) / n
    else:
        return (P - N) / n

def mk_ci(y, B=1000, alpha=0.05):
    """Bootstrap confidence interval"""
    n = len(y)
    mk_boot = np.zeros(B)
    for b in range(B):
        idx = np.random.choice(n, n, replace=True)
        y_boot = np.sort(y[idx])  # assumes uniform x
        mk_boot[b] = mk_coefficient(y_boot)
    return np.percentile(mk_boot, [100*alpha/2, 100*(1-alpha/2)])

def mk_test(y, B=1000):
    """Permutation test"""
    mk_obs = mk_coefficient(y)
    n = len(y)
    mk_perm = np.zeros(B)
    for b in range(B):
        y_perm = np.random.permutation(y)
        mk_perm[b] = mk_coefficient(y_perm)
    return np.mean(np.abs(mk_perm) >= np.abs(mk_obs))
