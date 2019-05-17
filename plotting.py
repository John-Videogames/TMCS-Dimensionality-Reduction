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


POSSIBLE_FILES = ['./Resources/trajectory_2019-05-16_03-49-27-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-44-22-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-43-00-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-03-39-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-48-20-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-48-54-PM.xyz',
                  './Resources/trajectory_2019-05-16_03-04-45-PM.xyz']

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


def plot_projections(possible_files, average_over_all=False):
    xyz_files = [XYZFile(filename) for filename in possible_files]
    # If we average over all, we create one 'master' xyz
    # file that contains all of them (rotated and scaled to
    # be at the same centre as xyz_files[0])
    if average_over_all:
        master_xyz = xyz_files[0]
        for xyz_file in xyz_files[1:]:
            master_xyz.append(xyz_file)
    else:
        # Otherwise, just use the first one.
        master_xyz = xyz_files[0]
    master_pca = PCAResults(master_xyz, 2)
    print(len(possible_files))
    fig, ax = plt.subplots()
    # ax.plot(master_pca.transformed_data[:, 0], master_pca.transformed_data[:, 1], "black")
    for xyz_file in xyz_files[1:]:
        transformed_data = master_pca.transform_data(xyz_file.frames)
        ax.plot(transformed_data[:, 0], transformed_data[:, 1])
    plt.show()


if __name__ == "__main__":
    input_file = XYZFile("./Resources/trajectory_2019-05-16_03-03-39-PM.xyz")
    pca_result = pca_from_xyz("./Resources/trajectory_2019-05-16_03-03-39-PM.xyz")


    energy_pca_2D(input_file,1,2)

    plot_projections(POSSIBLE_FILES)
    plot_projections(POSSIBLE_FILES, True)
