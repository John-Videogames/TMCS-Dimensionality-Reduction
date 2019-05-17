import matplotlib
matplotlib.use("TkAgg")

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from preprocessing import *
from processing import *
from sklearn.decomposition import PCA
from main import *
from matplotlib.pyplot import cm


def cumulative_variance():

    # empty lists for importing data and plotting
    inputxyzs = []
    PCA_test = []
    all_cumulative_variances = []
    component = list(range(26))

    # get data from .xyz files
    for file in POSSIBLE_FILES:

        xyzresult = XYZFile(file)
        inputxyzs.append(xyzresult)
        PCA_test.append(PCAResults(xyzresult,25))

    # loop over all input files
    for i in range(len(inputxyzs)):

        # calculate variance
        input_values = PCA_test[i].get_comp_variance()

        # calculate total variance across all principle components
        total_variance = 0.
        for i in range(len(input_values)):
            total_variance += input_values[i]

        # Set up lists/values for plotting
        cumulative_variances = [0]    # y-axis values
        cum_variance = 0.

        # get data to plot from input values
        for j in range(len(input_values)):
            cum_variance += input_values[j]/ total_variance
            cumulative_variances.append(cum_variance)

        # nested lists for plotting multiple trajectories on one graph
        all_cumulative_variances.append(cumulative_variances)

    # ---------------------------- plotting ------------------------------- #

    fig = plt.figure(figsize = (5,5))
    ax = fig.add_subplot(111)
    xmin, xmax = -1,25
    ymin, ymax = 0,1.1

    for k in range(len(all_cumulative_variances)):
       ax.plot(component,all_cumulative_variances[k],label = 'trajectory %s'%int(k+1), marker = '+')

    plt.legend(loc='best')
    ax.set_xlabel('Number of components')
    ax.set_ylabel('Cumulative variance')
    ax.set_title("Cumulative variances of the trajectories")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    fig.show()
    fig.savefig('cumulative_variances.png')


if __name__ == "__main__":

    cumulative_variance()
