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
    
    def __init__(self, input_object):
        self.input_object = input_object
        self.pca = PCA().fit(input_object.frames)
        
    def get_comp_variance(self):
        """Return variance for each PCA component"""
        return self.pca.explained_variance_ratio_
    
    def get_nth_eigenvector(self, number):
        """Retrun eigenvector number"""
        return self.pca.components_[number-1]
    
    def get_all_eigenvectors(self):
        """Return all eigenvectors"""
        return self.pca.components_
    

if __name__ == "__main__":
    # From preprocessing: create input_file
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    print(input_file.frames.shape)
    # Example how to use the PCAResults class
    # create PCA object
    PCA_test = PCAResults(input_file) 
    # Obtain variance for all PCA components as array
    variances = PCA_test.get_comp_variance()
    # Obtain nth eigenvector as array
    eigenvector_1 = PCA_test.get_nth_eigenvector(1)
    # Obtain all eigenvectors as matrix
    eigenvector_matrix = PCA_test.get_all_eigenvectors()
