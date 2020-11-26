import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('opencv_logo.png')
rows,cols,ch = img.shape

pts1 = np.float32([[51,158],[139,350],[150,20]])
pts2 = np.float32([[100,260],[290,64],[101,125]])
m = cv2.getAffineTransform(pts1,pts2)
dst = cv2.warpAffine(img,m,(cols,rows))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()