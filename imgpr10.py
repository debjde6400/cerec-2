import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('Lenna2.jpg')
rows,cols,ch = img.shape

pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])

m = cv2.getAffineTransform(pts1,pts2)
dst = cv2.warpAffine(img,m,(cols,rows))

plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.subplot(122),plt.imshow(img),plt.title('Output')
plt.show()