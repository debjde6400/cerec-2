import numpy as np
import cv2

#Load an image in grayscale
img = cv2.imread('Pic/Lenna.jpg')
#for i in range(50):
#     img[123+i,221+i*2] = [0,0,0]
apc = img[21:410, 111:361]
img[0:389, 0:250] = apc
bpc = img[11:33, 1:24]
img[34:56, 117:140] = bpc
cv2.imshow('An image',img)

k = cv2.waitKey(0)
if k==27 :
     cv2.destroyAllWindows()
elif k ==ord('s'):
     cv2.imwrite('Pic/Lenna2.jpg',img)
