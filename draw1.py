import numpy as np
import cv2

img = np.zeros((512,512,3),np.uint8)
img = cv2.circle(img,(256,256),50,(0,1,218),-1)
img = cv2.rectangle(img,(254,187),(327,254),(21,111,80),5)
img = cv2.rectangle(img,(184,258),(258,330),(21,111,80),5)

cv2.imshow('A drawing',img)
cv2.waitKey(0)
cv2.destroyAllWindows()