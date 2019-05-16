#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TMCS Dimensionality Reduction docstring
"""

from preprocessing import *
from processing import *
from plotting import *

if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    print(input_file.frames.shape)
    PCA_test = PCAResults(input_file)
    print(PCA_test.pca.components_)
