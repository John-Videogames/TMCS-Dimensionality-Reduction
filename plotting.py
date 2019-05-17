#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plotting module docstring goes here
"""

import numpy as np
from preprocessing import *
from processing import *
from sklearn.decomposition import PCA

if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    PCA_test = PCAResults(input_file) 

