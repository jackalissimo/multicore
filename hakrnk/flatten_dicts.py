import gc


def get_next_row(d: dict):
    for k, v in d.items():
        if isinstance(v, dict):
            for pair in get_next_row(v):
                yield k, *pair
        else:
            yield k, v


def flatten_dict(d: dict):
    res = {}
    for row in get_next_row(d):
        # print('gc: ', gc.get_count())
        ktup = map(str, row[:-1])
        v = row[-1]
        k = '.'.join(ktup)
        res[k] = v
    return res


def test():
    d1 = {}
    d2 = {'a': 1, 'b': 2}
    d3 = {'a': {'b': 2, 'c': 3}, 'd': 4}
    d4 = {'a': {'b': 2, 'c': {'c21': 33, 'c22': 34}}, 'd': 4}

    s1 = {}
    s2 = {'a': 1, 'b': 2}
    s3 = {'a.b': 2, 'a.c': 3, 'd': 4}
    s4 = {'a.b': 2, 'a.c.c21': 33, 'a.c.c22': 34, 'd': 4}

    assert s1 == flatten_dict(d1)
    assert s2 == flatten_dict(d2)
    assert s3 == flatten_dict(d3)
    assert s4 == flatten_dict(d4)

test()
