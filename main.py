#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TMCS Dimensionality Reduction docstring
"""
import os
from preprocessing import *
from processing import *
from plotting import *
print(os.listdir("./Resources/"))
POSSIBLE_FILES = ['trajectory_2019-05-16_03-49-27-PM.xyz',
                  'trajectory_2019-05-16_03-44-22-PM.xyz',
                  'trajectory_2019-05-16_03-43-00-PM.xyz',
                  'trajectory_2019-05-16_03-03-39-PM.xyz',
                  'trajectory_2019-05-16_03-48-20-PM.xyz',
                  'trajectory_2019-05-16_03-48-54-PM.xyz',
                  'trajectory_2019-05-16_03-04-45-PM.xyz']

if __name__ == "__main__":
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    PCA_test = PCAResults(input_file)

