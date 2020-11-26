import cv2
import numpy as np

img = cv2.imread('Pic/Lenna.jpg',0)
rows,cols = img.shape

m=np.float32([[1,0,200],[0,1,150]])
dst = cv2.warpAffine(img,m,(rows,cols))

cv2.imshow('img',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()