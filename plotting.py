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

    if comp3 == None:
        plt.scatter(transformed_data[comp1-1],transformed_data[comp2-1], c=energy_data)
        plt.xlabel("PC" + str(comp1))
        plt.ylabel("PC" + str(comp2))
        cbar = plt.colorbar()
        cbar.set_label("energy in kcal", labelpad=+1)
        plt.plot(transformed_data[comp1-1],transformed_data[comp2-1])
        # starting point
        plt.scatter(transformed_data[comp1 - 1][0], transformed_data[comp2 - 1][0], marker="x", c="red", label = "start")
        # end point
        plt.scatter(transformed_data[comp1 - 1][-1], transformed_data[comp2 - 1][-1], marker="s", c="red", label = "end")
        plt.legend()
        plt.title(i[12:-4] +"\nPC spanning a variance of %.3f" % (np.sum(PCA_object.get_comp_variance()[:2])))
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
        # starting point
        ax.scatter(transformed_data[comp1 - 1][0], transformed_data[comp2 - 1][0],transformed_data[comp3 - 1][0], marker="x", c="red", label="start")
        # end point
        ax.scatter(transformed_data[comp1 - 1][-1], transformed_data[comp2 - 1][-1],transformed_data[comp3 - 1][-1], marker="s", c="red", label="end")
        ax.legend()
        ax.set_title(i[12:-4] +"\nPC spanning a variance of %.3f" % (np.sum(PCA_object.get_comp_variance()[:3])))

    plt.savefig("Outputs/" + i[12:-4] + "2D.pdf")
    #plt.show()
    plt.close()


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
        input_file.minimise_rmsd()
        input_file.write_out(XYZ_object.filename[:-4] + "_comp" + str(i) + ".xyz")

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

    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.title("Motion in a common PCA space")
    if average_over_all:
        plt.savefig("./Outputs/projected-pca-averaged-projection.pdf")
    else:
        plt.savefig("./Outputs/projected-pca.pdf")

if __name__ == "__main__":
    #input_file = XYZFile("./Resources/trajectory_2019-05-16_03-03-39-PM.xyz")
    #pca_result = pca_from_xyz("./Resources/trajectory_2019-05-16_03-03-39-PM.xyz")

    #plot_projections(POSSIBLE_FILES)
    #plot_projections(POSSIBLE_FILES, True)
    #input_file = XYZFile('./Resources/trajectory_2019-05-16_03-49-27-PM.xyz')

    plot_projections(POSSIBLE_FILES)
    plot_projections(POSSIBLE_FILES, True)
    input_file = XYZFile('./Resources/trajectory_2019-05-16_03-49-27-PM.xyz')
    pca_result = PCAResults(input_file)
    comp = [i for i in range(pca_result.num_important_components(0.75))]
    get_xyz_for_specific_pc(input_file, comp)
    # Test for energy_bar_pca_plot() function
    # input_file = XYZFile('./Resources/trajectory_2019-05-16_03-49-27-PM.xyz')
    # energy_bar_pca_plot(input_file,1,2,3)

    for inputXYZ in POSSIBLE_FILES:
        pca_result = pca_from_xyz(inputXYZ)
        meaningful_components = pca_result.num_important_components(0.9)
        print(meaningful_components)
        get_xyz_for_specific_pc(XYZFile(inputXYZ),range(meaningful_components))

    #Test for energy_bar_pca_plot() function
    #input_file = XYZFile('./Resources/trajectory_2019-05-16_03-49-27-PM.xyz')
    #energy_bar_pca_plot(input_file,1,2)

    # Test for get_xyz_for_specific_pc() function
    # input_file = XYZFile('./Resources/malonaldehyde_IRC.xyz')
    # comp = [1,2]
    # get_xyz_for_specific_pc(input_file,comp)
    #Test for get_xyz_for_specific_pc() function
    #input_file = XYZFile('./Resources/malonaldehyde_IRC.xyz')
    #comp = [1,2]
    #get_xyz_for_specific_pc(input_file,comp)

    plt.close()
    for i in POSSIBLE_FILES:
        input_file = XYZFile(i)
        energy_bar_pca_plot(input_file,1,2)
