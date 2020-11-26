import numpy as np
import cv2

img1 = cv2.imread('Fire-In-The-Sky.jpg')
img2 = cv2.imread('space_planets.jpg')
for i in range(100):
    cv2.imshow('Image',cv2.addWeighted(img1,i/100,img2,1-(i/100),10))
    for j in range(100):
       pass
cv2.waitKey(0)
cv2.destroyAllWindows()