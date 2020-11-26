import numpy as np
import cv2

#Load an image in grayscale
img = cv2.imread('Pic/Lenna.jpg',0)
cv2.imshow('An image',img)
k = cv2.waitKey(0)
if k==27 :
     cv2.destroyAllWindows()
elif k ==ord('s'):
     cv2.imwrite('Pic/Lenna2.jpg',img)
