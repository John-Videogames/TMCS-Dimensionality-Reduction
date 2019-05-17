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
    pca_result = pca_from_xyz("./Resources/trajectory_2019-05-16_03-03-39-PM.xyz")
    pass

