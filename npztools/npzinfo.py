#!/usr/bin/env python
from __future__ import print_function
import numpy as np


"""
a script to display the content of a .npz file

11/02/2020
"""


def shapeformat(shape):
    return str(shape).replace('(', '')\
        .replace(')', '')\
        .replace(' ', '')\
        .replace(',', 'x').strip().strip('x')


def sizeformat(size):
    if size == 0:
        return "0"

    n = 0
    bkmg = []
    while size and n < 4:
        bkmg.append(int(size % 1024))
        size = size // 1024
        n += 1
    return str(bkmg[-1]) + " KMG"[len(bkmg) - 1]


def npzinfo(npzfile, long=False):
    assert npzfile.endswith('.npz')

    print(npzfile, ':')
    fmt  = "{:>25s} {:10s} {:10s} {:10s} {:s}"
    header = fmt.format('key', 'shape', 'dtype', 'size', 'value')
    print(header)
    with np.load(npzfile, allow_pickle=True) as loader:
        for key in loader.files:
            if long:
                value = loader[key]
                if str(value.shape) == "()":
                    value = value[()]
                value = str(value)
                value = ("\n" + 43 * " ").join([_.strip() for _ in value.split('\n')])
            else:
                value = "..."
                if str(loader[key].shape) == "()":
                    value = loader[key][()]
                    value = "{:20s}".format(str(value))
                    if "\n" in value:
                        value = value.split('\n')[0] + " ..."

            print(fmt.format(key,
                             shapeformat(loader[key].shape),
                             str(loader[key].dtype),
                             sizeformat(loader[key].itemsize * loader[key].size),
                             value))


if __name__ == "__main__":
    import sys
    long = "-l" in sys.argv[1:]
    npzfiles = [_ for _ in sys.argv[1:] if _.endswith('.npz')]
    for npzfile in npzfiles:
        npzinfo(npzfile, long=long)

