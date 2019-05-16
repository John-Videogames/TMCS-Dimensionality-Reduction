<<<<<<< HEAD
"""Code to process the input matrix via PCA"""
=======
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Processing docstring
"""
>>>>>>> 127386c28d23276ff97d3914333adc7a7c61ec78

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
<<<<<<< HEAD
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
        
if __name__ == "__main__":
    
    input_file = XYZFile("./Resources/malonaldehyde_IRC.xyz")
    
    #Example how to use the PCAResults class
    #create PCA object
    PCA_test = PCAResults(input_file) 
    #obtain variance for all PCA components as array
    variances = PCA_test.get_comp_variance()
    
=======
from preprocessing import *
from sklearn.decomposition import PCA


if __name__ == "__main__":
    pass
>>>>>>> 127386c28d23276ff97d3914333adc7a7c61ec78
