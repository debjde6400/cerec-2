import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('Face2.jpg')
b,g,r = cv2.split(img)
img =cv2.merge([r,g,b])
rows,cols,ch = img.shape

pts1= np.float32([[156,265],[138,452],[328,87],[39,130]])
pts2= np.float32([[0,0],[400,0],[0,400],[400,400]])
m = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,m,(400,400))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()