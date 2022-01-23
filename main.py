import csv
import numpy as np
import math
import sys

from matplotlib import pyplot as plt
from os import makedirs
from os.path import exists, join, dirname, relpath
from subprocess import check_call

OUT_DIR = join(dirname(__file__), 'out')
NUM_BITS = 12

def main():
    makedirs(OUT_DIR, exist_ok=True)
    data_file = join(OUT_DIR, f'estimated-complexities-{NUM_BITS}-bits.csv')
    if not exists(data_file):
        check_call([
            'Rscript', 'estimate-kolmogorov-complexities.R',
            str(NUM_BITS), data_file
        ])
    with open(data_file, 'r') as f:
        est_complexities = [float(line.rstrip()) for line in f]
    grid = get_grid(NUM_BITS)
    result = np.vectorize(lambda x: est_complexities[x])(grid)
    plt.imshow(result, cmap="gray")
    png_file = join(OUT_DIR, f'complexities-{NUM_BITS}-bits.png')
    plt.savefig(png_file)
    print('Generated ' + relpath(png_file))

"""
Returns a 2-d array of numbers 0 .. 2^NUM_BITS, arranged in such a way that each
cell's neighbors have exactly one bit flipped.
"""
def get_grid(NUM_BITS):
    if NUM_BITS == 1:
        return np.array([[0, 1]])
    result = get_grid(NUM_BITS - 1)
    if result.shape[1] < result.shape[0]:
        result = np.transpose(result)
    bottom = np.flip(np.bitwise_or(2 ** (NUM_BITS - 1), result), 0)
    return np.vstack([result, bottom])

def as_binary(a):
    return np.vectorize(np.binary_repr)(a, width=math.ceil(np.log2(np.max(a))))

def test():
    assert np.all(get_grid(1) == np.array([[0, 1]]))
    assert np.all(get_grid(2) == np.array([[0, 1],
                                           [2, 3]]))
    assert np.all(get_grid(3) == np.array([[0, 1],
                                           [2, 3],
                                           [6, 7],
                                           [4, 5]]))
    assert np.all(get_grid(4) == np.array([[0, 2, 6, 4],
                                           [1, 3, 7, 5],
                                           [9, 11, 15, 13],
                                           [8, 10, 14, 12]])), get_grid(4)

if __name__ == '__main__':
    main()