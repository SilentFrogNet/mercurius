from math import log2


def pretty_size(size):
    _suffixes = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    # determine binary order in steps of size 10
    # (coerce to int, // still returns a float)
    order = int(log2(size) / 10) if size else 0
    # format file size
    # (.4g results in rounded numbers for exact matches and max 3 decimals,
    # should never resort to exponent values)
    diff = order-len(_suffixes)+1
    order = order if diff <= 0 else len(_suffixes)-1
    return '{:.2f} {}'.format(size / (1 << (order * 10)), _suffixes[order])
