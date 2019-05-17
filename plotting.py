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
from mpl_toolkits.mplot3d import Axes3D


def energy_bar_pca_plot(XYZ_object, comp1, comp2, comp3 = None):
    """
    plotting PCA components against each other (2 or 3) and color them according to the energy
    :param XYZ_object:
    :param comp1:
    :param comp2:
    :param comp3:
    :return:
    """
    PCA_object = PCAResults(XYZ_object)
    PCA_object.transform_data()
    transformed_data = PCA_object.get_transformed_data()
    energy_data = XYZ_object.energy_frames

    print(energy_data)
    if comp3 == None:
        plt.scatter(transformed_data[comp1-1],transformed_data[comp2-1], c=energy_data)
        plt.xlabel("PC" + str(comp1))
        plt.ylabel("PC" + str(comp2))
        cbar = plt.colorbar()
        cbar.set_label("energy in kcal", labelpad=+1)
        plt.plot(transformed_data[comp1-1],transformed_data[comp2-1])
    else:
        fig = plt.figure()
        ax = Axes3D(fig)
        p = ax.scatter(transformed_data[comp1 - 1], transformed_data[comp2 - 1], transformed_data[comp3 - 1], c=energy_data)
        ax.set_xlabel("PC" + str(comp1))
        ax.set_ylabel("PC" + str(comp2))
        ax.set_zlabel("PC" + str(comp3))
        cbar = fig.colorbar(p)
        cbar.set_label("energy in kcal", labelpad=+1)
        ax.plot(transformed_data[comp1 - 1], transformed_data[comp2 - 1],transformed_data[comp3 - 1] )
    plt.show()

def get_xyz_for_specific_pc(XYZ_object, components):
    """
    performs PCA and gives xyz files of specific components
    :param XYZ_object:
    :return:
    """
    PCA_object = PCAResults(XYZ_object)
    PCA_object.transform_data()

    for i in components:
        input_file.frames = PCA_object.get_specific_inversetransformed_component(i)
        input_file.write_out(XYZ_object.filename[:-4] + "_comp" + str(i) + ".xyz")

if __name__ == "__main__":
    #Test for energy_bar_pca_plot() function
    #input_file = XYZFile('./Resources/trajectory_2019-05-16_03-49-27-PM.xyz')
    #energy_bar_pca_plot(input_file,1,2,3)

    #Test for get_xyz_for_specific_pc() function
    #input_file = XYZFile('./Resources/malonaldehyde_IRC.xyz')
    #comp = [1,2]
    #get_xyz_for_specific_pc(input_file,comp)