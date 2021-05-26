#!/usr/bin/env python
from npztools import Container
import sys, glob, os
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    npyfile = sys.argv[1]

    assert npyfile.endswith('.npy'), npyfile
    arr = np.load(npyfile)

    if arr.ndim == 2:
        plt.colorbar(plt.imshow(arr))

    elif arr.ndim == 1:
        plt.plot(arr)

    else:
        raise ValueError(npyfile)

    plt.show()
