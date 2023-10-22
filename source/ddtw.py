from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

##adapted from: https://github.com/z2e2/fastddtw

def generate_window(len_d_seq1, len_d_seq2, K):
    '''
    Generate reduced search space.
    '''
    
    for i in range(len_d_seq1):
        lb = max(0, i - K)
        ub = min(i + K, len_d_seq2)
        for j in range(lb, ub):
            yield (i + 1, j + 1)

def ddtw_distance(seq1, seq2, K = 10):
    '''
    Computes distance between two sequences using DDTW
    '''
    #computing derivative estimate of each seqnal
    seq1, seq2 = seq = np.array(seq1), np.array(seq2)
    d_seq = lambda s: ((s[1:-1] - s[:-2]) + (s[2:] - s[:-2])/2)/2
    d_seq1, d_seq2 = d_seq(seq1), d_seq(seq2)
    len_d_seq1, len_d_seq2 = len(d_seq1), len(d_seq2)

    #K = max(len(d_seq1), len(d_seq2)) // 10
    
    K = max(K, 2 * abs(len(d_seq1) - len(d_seq2)))
    window = generate_window(len_d_seq1, len_d_seq2, K)

    D = defaultdict(lambda: (float('inf'),))
    D[0, 0] = (0, 0, 0)

    for i, k in window:
        dt = abs(d_seq1[i-1] - d_seq2[k-1])
        case1 = (D[i-1, k][0]+dt, i-1, k)
        case2 = (D[i, k-1][0]+dt, i, k-1)
        case3 = (D[i-1, k-1][0]+dt, i-1, k-1)
        D[i, k] = min(case1, case2, case3, key = lambda a: a[0])

    return D[len_d_seq1, len_d_seq2][0]


    




