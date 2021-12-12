"""
https://www.hackerrank.com/challenges/maximize-it/problem

K M
K lines of Ni elements
K: 1..7
M: 1...1000
N: 1..7
Ni: 1... 1000_000_000

f = X ** 2
S = (f(X1) + f(X2) +...+f(Xk)) % M
    # must pick up exactly 1 from each of K arrays
TODO:
find max S
"""
from typing import List, Iterable
import itertools


def f(X):
    return X ** 2


def the_func(Xi: Iterable, M: int):
    return sum([f(x) for x in Xi]) % M


def gen_vec(lists: List[list]):
    """
    the best way to write unpredictable amount of nested for-loops:
    """
    prod = itertools.product(*lists)
    for p in prod:
        yield p


def solution(K: int, M: int, N: list, lists: List[list]):
    max_ = 0
    max_vec = []
    for vec in gen_vec(lists):
        res = the_func(vec, M)
        # print(vec, res)
        if res > max_:
            max_ = res
            max_vec = vec
    return max_



input_ = input


inp = inp1 = """
3 1000
2 5 4
3 7 8 9
5 5 7 8 9 10
""".strip()
exp1 = 206

it = None
def make_it():
    global it
    it = iter(inp.split('\n'))

def input_():
    def inner():
        global it
        try:
            yield next(it)
        except Exception:
            make_it()
            yield next(it)
    return next(inner())


def proceed_input(exp: int):
    K, M = map(int, input_().split(' '))
    lists = []
    N = []
    for i in range(K):
        els = list(map(int, input_().split(' ')))
        N.append(els[0])
        lists.append(els[1:])
    sol = solution(K, M, N, lists)
    print(sol)
    assert exp == sol

def test1():
    global exp1
    proceed_input(exp1)

def test2():
    global inp
    inp = """
3 1000
2 5 4001
3 7 50999 9
5 5 7 60998 9 10
""".strip()
    proceed_input(exp=206)

test1()
test2()
