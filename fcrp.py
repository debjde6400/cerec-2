import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('..\\opencv\\build\\data\\haarcascades\\haarcascade_frontalface_default.xml')
#point : \\ is to be used instead of \

def face_crop(fpath):
  global face_cascade
  img = cv2.imread(fpath)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray,1.5,1)
  i=1
  fn=fpath[fpath.rindex('/')+1:len(fpath)]

  for(x,y,w,h) in faces :
     cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),1)
     roi_gray = gray[y:y+h,x:x+w]
     roi_color = img[y:y+h,x:x+w]
     cv2.imwrite(fn+'_Face'+str(i)+'.jpg',roi_color)
     i=i+1
