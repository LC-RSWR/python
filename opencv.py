import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('C:/Users/deskadmin/Desktop/863/1.png')
kernel = np.ones((5,5),np.float32)/25
dst = cv.filter2D(img,-1,kernel)
blur_1 = cv.GaussianBlur(img,(5,5),0)
blur_2 = cv.bilateralFilter(img,9,75,75)
plt.figure(figsize=(10,10))
plt.subplot(221),plt.imshow(img[:,:,::-1]),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(dst[:,:,::-1]),plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(blur_1[:,:,::-1]),plt.title('Gaussian')
plt.xticks([]), plt.yticks([])
plt.subplot(224),plt.imshow(blur_1[:,:,::-1]),plt.title('Bilateral')
plt.xticks([]), plt.yticks([])
plt.show()
