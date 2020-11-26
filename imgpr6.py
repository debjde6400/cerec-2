import numpy as np
import cv2

img1 = cv2.imread('Pic/Lenna.jpg')
img2 = cv2.imread('Pic/Lenna2.jpg')

dst = cv2.addWeighted(img1,0.65,img2,0.35,0)

cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

img1 = cv2.imread('Pic/Fire-In-The-Sky.jpg')
img2 = cv2.imread('Pic/3D-Wallpapers-HD-Wallpapers.jpg')

dst2 = cv2.addWeighted(img1,0.44,img2,0.64,0)
cv2.imwrite('Fusion1.jpg',dst2)
cv2.imshow('Fusion1.jpg',dst2)

cv2.waitKey(0)
cv2.destroyAllWindows()
