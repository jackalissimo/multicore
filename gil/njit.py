"""
sometimes we don't need GIL
"""
import numpy as np
from timeit import default_timer as timer
from numba import jit, njit

x = np.arange(40000).reshape(200, 200)
N = 10000


def go_slow(a):
    trace = 0.0
    for i in range(a.shape[0]):
        trace += np.tanh(a[i, i])
    return a + trace


# @jit(nopython=True)
@njit
def go_fast(a):
    trace = 0.0
    for i in range(a.shape[0]):
        trace += np.tanh(a[i, i])
    return a + trace


def main():
    start = timer()
    for i in range(N):
        go_slow(x)
    finish = timer()
    print("go_slow: %.3f" % (finish - start, ))

    start = timer()
    go_fast(x)
    finish = timer()
    print("go_fast, compilation: %.3f" % (finish - start, ))

    start = timer()
    for i in range(N):
        go_fast(x)
    finish = timer()
    print("go_fast, after compilation: %.3f" % (finish - start, ))

if __name__ == '__main__':
    main()
