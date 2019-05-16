import matplotlib
matplotlib.use("TkAgg")

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from preprocessing import *
from processing import *
from sklearn.decomposition import PCA



# get data from .xyz file
input_file = XYZFile("./Resources/trajectory_2019-05-16_03-49-27-PM.xyz")
PCA_test = PCAResults(input_file)

# get variance from input files
input_values = PCA_test.get_comp_variance()

# calculate total variance
total_variance = 0.
for i in range(len(input_values)):
    total_variance += input_values[i]


# Set up lists/values for plotting
variance = []
component = [0]               # x-axis values
cumulative_variances = [0]    # y-axis values
cum_variance = 0.

# get data to plot from input values
for i in range(len(input_values)):
    component.append(i + 1)
    cum_variance += input_values[i]/ total_variance
    cumulative_variances.append(cum_variance)


# ------------------ plotting ------------------ #

fig = plt.figure(figsize = (5,5))
ax = fig.add_subplot(111)

xmin, xmax = -1,25
ymin, ymax = 0,1.1
ax.plot(component, cumulative_variances, c = 'r' )
ax.set_xlabel('Number of components')
ax.set_ylabel('Cumulative variance')
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)
plt.savefig('variances_trajectory_2019-05-16_03-49-27-PM.png')



