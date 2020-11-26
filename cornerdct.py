import cv2
import numpy as np

img = cv2.imread('Lenna2.jpg')
gray = np.float32(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
dst = cv2.dilate(cv2.cornerHarris(gray,2,3,0.04),None)
img[dst>0.01*dst.max()] = [0,255,255]

cv2.imshow('dst',img)

if cv2.waitKey(0) & 0xff ==27 :
     cv2.destroyAllWindows()