import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('Pic/Fire-In-The-Sky.jpg')
b,g,r = cv2.split(img)
img2 = cv2.merge([r,g,b])
plt.imshow(img2, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]),plt.yticks([])
plt.show()