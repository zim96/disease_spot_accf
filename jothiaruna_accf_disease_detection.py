import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import cv2 as cv
from skimage import filters
import glob

def im2double(im, min_val, max_val):    
    return (im.astype('float') - min_val) / (max_val - min_val)

"""
Re-map pixel values using Excess Red (ExR)
"""
def apply_ExR(img):
    result_img = (1.3*img[:,:,0]) - img[:,:,1]

    return result_img

"""
Truncated SVD decolor of image
"""
def TruncSVDdecolor(img, r):
    img_lab = cv.cvtColor(img, cv.COLOR_RGB2LAB)

    ## Compute SVD
    U_a, S_a, VT_a = np.linalg.svd(img_lab[:,:,1], full_matrices=False)
    U_b, S_b, VT_b = np.linalg.svd(img_lab[:,:,2], full_matrices=False)

    S_a = np.diag(S_a)
    S_b = np.diag(S_b)

    img_a_approx = U_a[:,:r] @ S_a[:r,:r] @ VT_a[:r,:]
    img_b_approx = U_b[:,:r] @ S_b[:r,:r] @ VT_b[:r,:]
    img_approx = img_a_approx + img_b_approx + img_lab[:,:,0]
    img_approx = np.stack([img_approx, img_approx, img_approx], axis=2)
    img_approx = np.mean(img_approx, -1)

    return img_approx

img_paths = glob.glob("D:/Datasets/PlantVillage/Pepper__bell___Bacterial_spot/*.JPG")
r = 50
N = 3

for path in img_paths:
    img = cv.imread(path)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    svd_decolor = TruncSVDdecolor(img, r)
    svd_decolor = ndimage.convolve(svd_decolor, np.ones((N,N))/(N*N))
    # print(np.unique(svd_decolor))

    hue = cv.cvtColor(img, cv.COLOR_RGB2HSV)[:,:,0]
    hue = filters.difference_of_gaussians(hue, low_sigma=4, high_sigma=5)
    # print(np.unique(hue))

    exr_img = apply_ExR(img)
    exr_img = ndimage.convolve(exr_img, np.ones((N,N))/(N*N))
    # print(np.unique(exr_img))

    accf = (0.1*exr_img) + svd_decolor + hue
    accf = accf*0.5
    # accf_bin = accf < filters.threshold_mean(accf)

    plt.subplot(221)
    plt.title("SVD Decolor")
    plt.axis('off')
    plt.imshow(svd_decolor, cmap='gray')
    plt.subplot(222)
    plt.title("Hue")
    plt.axis('off')
    plt.imshow(hue, cmap='gray')
    plt.subplot(223)
    plt.title("ExR")
    plt.axis('off')
    plt.imshow(exr_img, cmap='gray')
    plt.subplot(224)
    plt.title("ACCF")
    plt.axis('off')
    plt.imshow(accf, cmap='gray')
    plt.show(block=False)
    plt.pause(2)
