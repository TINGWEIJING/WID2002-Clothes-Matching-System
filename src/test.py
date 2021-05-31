from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math

# Nearest Neighbor Interpolation Algorithm
# dstH is the height of the new image; dstW is the width of the new image


def NN_interpolation(img, dstH, dstW):
    print(img.shape)
    scrH, scrW, channels = img.shape
    retimg = np.zeros((dstH, dstW, channels), dtype=np.uint8)
    for i in range(dstH):
        for j in range(dstW):
            scrx = round(i*(scrH/dstH))
            scry = round(j*(scrW/dstW))
            retimg[i, j] = img[scrx, scry]
    return retimg


im_path = './src/yellow.jpg'
image = np.array(Image.open(im_path))

image1 = NN_interpolation(image, int(image.shape[0]*0.5), int(image.shape[1]*0.5))
image1 = Image.fromarray(image1.astype('uint8')).convert('RGB')
image1.save('./src/out.png')
