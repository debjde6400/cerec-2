import numpy as np
import cv2

img1 = cv2.imread('myimg1.jpg',0)

img2 = cv2.threshold(img1,124,255,cv2.THRESH_BINARY)

img =cv2.bitwise_and(img1,img2)

cv2.imshow("Result of threshold 'and'",img)

cv2.waitKey(0)
cv2.destroyAllWindows() 