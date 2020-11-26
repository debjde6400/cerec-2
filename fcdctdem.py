import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('..\\opencv\\build\\data\\haarcascades\\haarcascade_frontalface_default.xml')
#point : \\ is to be used instead of \
img = cv2.imread('DSC01959.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray,1.5,1)

for(x,y,w,h) in faces :
   cv2.rectangle(img,(x,y),(x+w,y+h),(12,234,112),2)
   roi_gray = gray[y:y+h,x:x+w]
   roi_color = img[y:y+h,x:x+w]

cv2.imshow('Image after detecting face',img)
cv2.waitKey(0)
cv2.destroyAllWindows()