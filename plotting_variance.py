import matplotlib
matplotlib.use("TkAgg")

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from preprocessing import *
from processing import *
from sklearn.decomposition import PCA
from main import *


def cumulative_variance():



    # empty lists for importing data and plotting
    inputxyzs = []
    PCA_test = []
    all_cumulative_variances = []
    output = range(26)  # THIS IS SUPPOSED TO BE OF LENGTH OF THE PRINCIPLE COMPONENTS??


    # get data from .xyz files
    for file in POSSIBLE_FILES:
        inputxyzs.append(XYZFile(file))
        PCA_test = PCAResults(inputxyzs[file])

    # loop over all input files
    for i in range(len(inputxyzs)):

        # calculate variance
        input_values = PCA_test[i].get_comp_variance()

        # calculate total variance across all principle components
        total_variance = 0.
        for i in range(len(input_values)):
            total_variance += input_values[i]

        # Set up lists/values for plotting
        component = [0]               # x-axis values
        cumulative_variances = [0]    # y-axis values
        cum_variance = 0.

        # get data to plot from input values
        for j in range(len(input_values)):
            component.append(j + 1)
            cum_variance += input_values[j]/ total_variance
            cumulative_variances.append(cum_variance)

        all_cumulative_variances.append(cumulative_variances)


        # ---------------------------- plotting ------------------------------- #

        fig = plt.figure(figsize = (5,5))
        ax = fig.add_subplot(111)

        xmin, xmax = -1,25
        ymin, ymax = 0,1.1
        ax.plot(component, cumulative_variances, c = 'r' )
        ax.set_xlabel('Number of components')
        ax.set_ylabel('Cumulative variance')
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.savefig('cumulative_variances.png')



