import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from time import time
from PIL import Image

n_colors = 2

def perform_Kmeans(image):
    # Convert to floats instead of the default 8 bits integer coding. Dividing by
    # 255 is important so that pl.imshow behaves works well on foat data (need to
    # be in the range [0-1]
    image = np.array(image, dtype=np.float64) / 255
    w, h, d = original_shape = tuple(image.shape)
    assert d == 3

    image_array = np.reshape(image, (w * h, d))

    # Fitting estimator on a small sub-sample of the data
    image_array_sample = shuffle(image_array, random_state=0)[:1000]
    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)

    # Get label for all points
    labels = kmeans.predict(image_array)

    # Return the image after k-means clustering
    return recreate_image(kmeans.cluster_centers_, labels, w, h)


def recreate_image(codebook, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image