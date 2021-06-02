import os
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl


# Number of cluster and iterations, larger iter = longer time
# Higher number of K retain more details of the original image
K = 10
max_iters = 1

# ignore the warning when divide by NaN
np.seterr(divide='ignore', invalid='ignore')

# Get the nearest centroids for each x
def findClosestCentroids(X, centroids):
    # Set K
    K = centroids.shape[0]
    idx = np.zeros(X.shape[0], dtype=int)

    for i in range(idx.size):
        J = np.sum(np.square(X[i] - centroids), axis=1)
        idx[i] = np.argmin(J) # Pick the centroid which gives minimum cost J

    return idx

# Compute the centroids, using mean of the points allocated under this centroid
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

    randidx = np.random.permutation(X.shape[0]) # Permutate the sequence from 1 ... m
    centroids = X[randidx[:K], :] # Pick first k value

    return centroids

def runkMeans(X, centroids, max_iters=10):
    K = centroids.shape[0]
    idx = None

    for i in range(max_iters):
        idx = findClosestCentroids(X, centroids)
        centroids = computeCentroids(X, idx, K)

    return centroids, idx



def perform(image):
    """
    image: OpenCV Image format
    """
    # Divide by 255, to make it in the range of 0 ... 1
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

    # Remove invalid (NaN) value from the centroids
    to_be_deleted = []
    for i in range(len(centroids)): # Search for invalid value, appending them into to_be_deleted
        for element in centroids[i]:
            if np.isnan(element):
                to_be_deleted.append(i)
                break
    centroids = np.delete(centroids, to_be_deleted, 0) # Remove the invalid row
    
    # Return the centroids and the clusted image in 255 colour code
    return np.array(np.dot(centroids, 255), dtype=np.uint8), np.array(np.dot(X_recovered, 255), dtype=np.uint8)