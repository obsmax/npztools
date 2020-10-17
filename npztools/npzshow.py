#!/usr/bin/env python
from npztools import Container
import sys, glob, os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    npzfile, key = sys.argv[1:]

    c = Container()
    c.loadkeys(npzfile, [key])

    if c[key].ndim == 2:
        plt.colorbar(plt.imshow(c[key]))
    elif c[key].ndim == 1:
        plt.plot(c[key])
    else:
        raise ValueError(npzfile, key)
    plt.show()
