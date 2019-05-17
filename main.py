#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TMCS Dimensionality Reduction docstring
"""
import os
from preprocessing import *
from processing import *
from plotting import *
import matplotlib.pyplot as plt
POSSIBLE_FILES = ['./Resources/trajectory_2019-05-16_03-49-27-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-44-22-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-43-00-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-03-39-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-48-20-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-48-54-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-04-45-PM.xyz']

if __name__ == "__main__":

    for file in POSSIBLE_FILES:
        input_file = XYZFile('./Resources/trajectory_2019-05-16_03-49-27-PM.xyz')
        PCA_test = PCAResults(input_file)
        print(PCA_test.num_important_components(0.90), "components are necessary to capture 90% of the variance")
    PCA_test.inversetransform_data()
    input_file.frames = PCA_test.get_inversetransform_data()
    print("Outputting")
    input_file.write_out("PCA_out_test.xyz")
