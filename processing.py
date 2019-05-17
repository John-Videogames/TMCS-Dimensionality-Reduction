"""Code to process the input matrix via PCA"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.decomposition import PCA
from preprocessing import *


class PCAResults:
    """
    Class to perform PCA on given input matrix and return processed results
    """
    
    def __init__(self, input_object, n_components=None):
        self.input_object = input_object
        self.data = self.input_object.frames
        self.n_components = n_components
        if n_components is None:
            # Doing full PCA fit
            self.pca = PCA().fit(self.data)
        else:
            # Doing PCA with n_components components
            self.pca = PCA(n_components).fit(self.data)
        self.transformed_data = self.transform_data()
        self.inversetransformed_data = None
        
    def get_comp_variance(self):
        """Return variance for each PCA component"""
        return self.pca.explained_variance_ratio_
    
    def get_nth_eigenvector(self, number):
        """Return eigenvector number"""
        return self.pca.components_[number-1]
    
    def get_all_eigenvectors(self):
        """Return all eigenvectors"""
        return self.pca.components_

    def transform_data(self, data=None):
        """
        Transform data based on fit.
        By default transforms its own data.
        """
        if data is None:
            data = self.data
        return self.pca.transform(data)


    def get_transformed_data(self):
        """Return matrix of transformed data"""
        if self.transformed_data is None:
            print("Data has not be transformed yet. Transformation will be done automatically now")
            self.transform_data()
        return self.transformed_data.T

    def inversetransform_data(self):
        """Inverse transform data"""
        if self.transformed_data is None:
            print("Data has not be transformed yet. Transformation will be done automatically now")
            self.transform_data()
        self.inversetransformed_data = self.pca.inverse_transform(self.transformed_data)

    def get_inversetransform_data(self):
        """Return inverse transform data"""
        if self.inversetransformed_data is None:
            print("Data has not been inverse transformed yet. Inverse transformation will be done automatically now")
            self.inversetransform_data()
        return self.inversetransformed_data

    def num_important_components(self, threshold):
        """
        Returns the number of components
        required to capture a certain
        amount of the variance.
        :param threshold:
        :return:
        """
        assert threshold <= 1.0 and threshold >= 0.0, "Threshold must be in the range (0.0, 1.0)"
        print(np.cumsum(self.pca.explained_variance_ratio_))
        return np.argmax(np.cumsum(self.pca.explained_variance_ratio_) > threshold)

    def get_specific_inversetransformed_component(self, component):
        """Return inverse transformed vector in original XYZ coordinates for a specific PCA component"""
        return np.dot(self.get_transformed_data().T[:, component - 1].reshape(-1,1), self.pca.components_[component-1].reshape(1,-1)) + self.pca.mean_


def pca_from_xyz(xyz_filename: str) -> PCAResults:
    """
    Turns an xyz filename into
    a transformed PCA result
    :type xyz_filename: str
    :param xyz_filename: 
    :return: 
    """
    in_xyz = XYZFile(xyz_filename)
    pca_result = PCAResults(in_xyz)
    pca_result.transform_data()
    return pca_result


if __name__ == "__main__":

    ###########################################
    #
    # Example how to use the PCAResults class
    #
    ###########################################

    # From preprocessing: create input_file
    input_file = XYZFile("./Resources/trajectory_2019-05-16_03-03-39-PM.xyz")
    pca_res = pca_from_xyz("./Resources/malonaldehyde_IRC.xyz")
    print(pca_res.num_important_components(0.90))
    # Create PCA object with full PCA
    PCA_test = PCAResults(input_file)
    # Obtain variance for all PCA components as array
    variances = PCA_test.get_comp_variance()
    # Obtain nth eigenvector as array
    eigenvector_1 = PCA_test.get_nth_eigenvector(1)
    # Obtain all eigenvectors as matrix
    eigenvector_matrix = PCA_test.get_all_eigenvectors()

    # Or create PCA object with PCA of n components, e.g. 2
    PCA_test_2 = PCAResults(input_file, 27)
    # Transform data based on PCA fit
    PCA_test_2.transform_data()

    # Example for plotting the transformed data in the coordinate system spanned by PC1 and PC2
    plt.scatter(PCA_test_2.get_transformed_data()[0], PCA_test_2.get_transformed_data()[1])
    plt.show()

    # Inverse transform data
    PCA_test_2.inversetransform_data()

    # Write inverse tranformed data as xyz - visualize in VMD
    input_file.frames = PCA_test_2.get_inversetransform_data()
    input_file.write_out("./Resources/trajectory_PCA_2019-05-16_03-03-39-PM.xyz")

    # Get one specific inverse transform
    input_file.frames = PCA_test_2.get_specific_inversetransformed_component(2)
    input_file.write_out("PCA_out_test2.xyz")







