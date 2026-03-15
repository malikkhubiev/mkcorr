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

def mk_ties_corrected(y):
    """Ties-corrected version of MK coefficient"""
    y = np.asarray(y)
    n = len(y)
    if n < 2:
        return 0.0
    
    diffs = np.sign(np.diff(y))
    P = np.sum(diffs > 0)
    N = np.sum(diffs < 0)
    T = np.sum(diffs == 0)
    S = np.sum(diffs)
    M = np.sign(S)
    
    denominator = n - T
    
    if M > 0:
        return (P + 1) / denominator
    elif M < 0:
        return -(N + 1) / denominator
    else:
        return (P - N) / denominator

def mk_ci(y, x=None, B=1000, alpha=0.05):
    """Bootstrap confidence interval for MK coefficient"""
    y = np.asarray(y)
    n = len(y)
    mk_boot = np.zeros(B)
    
    for b in range(B):
        idx = np.random.choice(n, n, replace=True)
        if x is not None:
            x_boot = np.asarray(x)[idx]
            y_boot = y[idx]
            sort_idx = np.argsort(x_boot)
            y_boot = y_boot[sort_idx]
        else:
            y_boot = np.sort(y[idx])
        
        mk_boot[b] = mk_coefficient(y_boot)
    
    return np.percentile(mk_boot, [100*alpha/2, 100*(1-alpha/2)])

def mk_test(y, x=None, B=1000):
    """Permutation test for MK coefficient"""
    y = np.asarray(y)
    if x is not None:
        x = np.asarray(x)
        sort_idx = np.argsort(x)
        y = y[sort_idx]
    
    mk_obs = mk_coefficient(y)
    n = len(y)
    mk_perm = np.zeros(B)
    
    for b in range(B):
        y_perm = np.random.permutation(y)
        mk_perm[b] = mk_coefficient(y_perm)
    
    p_value = np.mean(np.abs(mk_perm) >= np.abs(mk_obs))
    return mk_obs, p_value
