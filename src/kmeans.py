import os
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl



# Number of cluster and iterations, larger K = longer time
K = 10
max_iters = 1

# Get the nearest centroids
def findClosestCentroids(X, centroids):
    # Set K
    K = centroids.shape[0]
    idx = np.zeros(X.shape[0], dtype=int)

    for i in range(idx.size):
        J = np.sum(np.square(X[i] - centroids), axis=1)
        idx[i] = np.argmin(J)

    return idx

# Compute the centroids
def computeCentroids(X, idx, K):
    m, n = X.shape
    centroids = np.zeros((K, n))
    for i in range(K):
        centroids[i] = np.mean(X[idx == i], axis=0) 
    return centroids

# Randomize the centroids
def kMeansInitCentroids(X, K):
    m, n = X.shape
    centroids = np.zeros((K, n))

    randidx = np.random.permutation(X.shape[0])
    centroids = X[randidx[:K], :]

    return centroids

def runkMeans(X, centroids, max_iters=10):

    K = centroids.shape[0]
    idx = None


    for i in range(max_iters):
        idx = findClosestCentroids(X, centroids)
        centroids = computeCentroids(X, idx, K)

    return centroids, idx



def perform(image):

    image = np.array(image, dtype=np.float64) / 255

    # Reshape the image into an Nx3 matrix where N = number of pixels.
    # Each row will contain the Red, Green and Blue pixel values
    # This gives us our dataset matrix X that we will use K-Means on.
    X = image.reshape(-1, 3)

    # Randomly initialise the centroids position
    initial_centroids = kMeansInitCentroids(X, K)

    # Run K-Means
    centroids, idx = runkMeans(X, initial_centroids, max_iters)

    # Reshape the recovered image into proper dimensions and convert to uint8
    X_recovered = centroids[idx, :].reshape(image.shape)

    # Return the centroids and the clusted image
    # centroids = centroids[np.logical_not(np.isnan(centroids))]
    to_be_deleted = []
    for i in range(len(centroids)):
        for element in centroids[i]:
            if np.isnan(element):
                to_be_deleted.append(i)
                break
    centroids = np.delete(centroids, to_be_deleted, 0)
    return np.array(np.dot(centroids, 255), dtype=np.uint8), np.array(np.dot(X_recovered, 255), dtype=np.uint8)