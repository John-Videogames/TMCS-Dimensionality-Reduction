import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits
from sklearn.datasets import fetch_lfw_people
from sklearn.decomposition import PCA as RandomizedPCA

def draw_vector(v0, v1, ax=None):
    """
    Function to draw the vectors based on a 2 component PCA
    :param v0:
    :param v1:
    :param ax:
    :return:
    """
    ax = ax or plt.gca()
    arrowprops=dict(arrowstyle='->',
                    linewidth=2,
                    shrinkA=0, shrinkB=0, color='black')
    ax.annotate('', v1, v0, arrowprops=arrowprops)
    
def plot_digits(data):
    fig, axes = plt.subplots(4, 10, figsize=(10, 4),
                             subplot_kw={'xticks':[], 'yticks':[]},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(data[i].reshape(8, 8),
                  cmap='binary', interpolation='nearest',
                  clim=(0, 16))

#Create random data set
rng = np.random.RandomState(1)
X = np.dot(rng.rand(2, 2), rng.randn(2, 200)).T

def tutorial_1():
    """Tutorial 1: Random 2D dataset rotated to PCA 2D"""

    #Set up the PCA and fit
    pca = PCA(n_components=2)
    pca.fit(X)

    #Data from fit
    print(pca.components_)
    print(pca.explained_variance_)

    #Set up a plot
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    # plot original data with PCA vectors
    ax1.scatter(X[:, 0], X[:, 1], alpha=0.2) #original data
    for length, vector in zip(pca.explained_variance_, pca.components_):
        v = vector * 3 * np.sqrt(length)
        draw_vector(pca.mean_, pca.mean_ + v, ax1)
    ax1.axis('equal')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')

    #plot pca data
    X_pca = pca.transform(X) #transform original data to pca coordinates
    ax2.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.2)
    ax2.set_ylim([-1,1])
    ax2.axis('equal')
    ax2.set_xlabel('PCA1')
    ax2.set_ylabel('PCA2')


    fig.tight_layout()
    
def tutorial_2():
    """Tutorial 2: Reduction of Dimensionality from 2D to 1D"""
    
    #PCA for eduction 2D -> 1D
    pca = PCA(n_components=1)
    pca.fit(X)
    X_pca = pca.transform(X)
    print("original shape:   ", X.shape)
    print("transformed shape:", X_pca.shape)
    
    #Plot reduction
    X_new = pca.inverse_transform(X_pca)
    plt.scatter(X[:, 0], X[:, 1], alpha=0.2)
    plt.scatter(X_new[:, 0], X_new[:, 1], alpha=0.8)
    plt.axis('equal');
    
def tutorial_3():
    """Tutorial 3: Reduction of Dimensionality 64D to 2D"""
    
    digits = load_digits()
    digits.data.shape
    
    pca = PCA(2)  # project from 64 to 2 dimensions
    projected = pca.fit_transform(digits.data)
    print(digits.data.shape)
    print(projected.shape)
    
    plt.scatter(projected[:, 0], projected[:, 1],
            c=digits.target, edgecolor='none', alpha=0.5,
            cmap=plt.cm.get_cmap('spring', 10))
    plt.xlabel('component 1')
    plt.ylabel('component 2')
    plt.colorbar();
    
    
def tutorial_4():
    """Tutorial 4: Evaluate how many PCA components are needed"""
    digits = load_digits()
    
    pca = PCA().fit(digits.data)
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance');
    

def tutorial_5():
    """Tutorial 5: Noise filtering"""
    
    digits = load_digits()
    plot_digits(digits.data)
    
    np.random.seed(42)
    noisy = np.random.normal(digits.data, 4)
    plot_digits(noisy)
    
    pca = PCA(0.50).fit(noisy)
    print(pca.n_components_)
    
    components = pca.transform(noisy)
    filtered = pca.inverse_transform(components)
    plot_digits(filtered)
    
def tutorial_6():
    """Tutorial 6: Eigenfaces"""
    
    faces = fetch_lfw_people(min_faces_per_person=60)
    print(faces.target_names)
    print(faces.images.shape)
    
    pca = RandomizedPCA(150)
    pca.fit(faces.data)
    
    
    
tutorial_6()
    



