"""Code to process the input matrix via PCA"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        if n_components == None:
            #doing full PCA fit
            self.pca = PCA().fit(self.data)
        else:
            #doing PCA with n_components components
            self.pca = PCA(n_components).fit(self.data)
        self.transformed_data = None
        
    def get_comp_variance(self):
        """Return variance for each PCA component"""
        return self.pca.explained_variance_ratio_
    
    def get_nth_eigenvector(self, number):
        """Retrun eigenvector number"""
        return self.pca.components_[number-1]
    
    def get_all_eigenvectors(self):
        """Return all eigenvectors"""
        return self.pca.components_
    
    def transform_data(self):
        """Transform data based on fit"""
        self.transformed_data = self.pca.transform(self.data)

    def get_transformed_data(self):
        """Return matrix of transformed data"""
        return self.transformed_data
        
if __name__ == "__main__":

    ###########################################
    #
    # Example how to use the PCAResults class
    #
    ###########################################

    # From preprocessing: create input_file
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")

    #create PCA object with full PCA
    PCA_test = PCAResults(input_file)
    # obtain variance for all PCA components as array
    variances = PCA_test.get_comp_variance()
    # obtain nth eigenvector as array
    eigenvector_1 = PCA_test.get_nth_eigenvector(1)
    # obtain all eigenvectors as matrix
    eigenvector_matrix = PCA_test.get_all_eigenvectors()

    #or create PCA object with PCA of n components, e.g. 2
    PCA_test_2 = PCAResults(input_file, 2)
    #transform data based on PCA fit
    PCA_test_2.transform_data()
    #Example for plotting the transformed data in the coordinate system spanned by PC1 and PC2
    plt.scatter(PCA_test_2.get_transformed_data().T[0], PCA_test_2.get_transformed_data().T[1])
    plt.show()






