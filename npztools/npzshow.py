#!/usr/bin/env python
from npztools import Container
import sys, glob, os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    npzfile = sys.argv[1]
    keys = sys.argv[2:]

    c = Container()
    c.loadkeys(npzfile, keys)

    if len(keys) == 1:
        # single key

        key = keys[0]
        if c[key].ndim == 2:
            plt.colorbar(plt.imshow(c[key]))
        elif c[key].ndim == 1:
            plt.plot(c[key])
        else:
            raise ValueError(npzfile, key)

    elif len(keys) == 2:
        # two keys

        key1, key2 = keys
        if c[key1].ndim == 1 and c[key2].ndim == 1 and len(c[key1]) == len(c[key2]):
            # 2D plot
            plt.plot(c[key1], c[key2])
        else:
            raise NotImplementedError(f'{key1}: {c[key1].shape}, {key2}: {c[key2].shape}')

    elif len(keys) == 3:
        key1, key2, key3 = keys
        plt.pcolormesh(c[key1], c[key2], c[key3])


    plt.show()
