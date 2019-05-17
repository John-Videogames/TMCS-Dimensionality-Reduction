#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plotting module docstring goes here
"""

import numpy as np
from preprocessing import *
from processing import *
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def energy_pca_2D(XYZ_object, comp1, comp2, comp3 = None):
    PCA_object = PCAResults(XYZ_object)
    PCA_object.transform_data()
    transformed_data = PCA_object.get_transformed_data()
    energy_data = XYZ_object.energy_frames

    print(energy_data)
    if comp3 == None:
        plt.scatter(transformed_data[comp1-1],transformed_data[comp2-1])
        plt.xlabel("PC" + str(comp1))
        plt.ylabel("PC" + str(comp2))
        
    plt.show()


if __name__ == "__main__":
    input_file = XYZFile("./Resources/trajectory_PCA_2019-05-16_03-03-39-PM.xyz")
    pca_result = pca_from_xyz("./Resources/trajectory_2019-05-16_03-03-39-PM.xyz")


    energy_pca_2D(input_file,1,2)