import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('Folder.jpg')

kernel = np.ones((5,5),np.float32)/25
t1 = cv2.filter2D(img,-1,kernel)
t2 = cv2.blur(img,(5,5))
t3 = cv2.GaussianBlur(img,(5,5),0)
t4 = cv2.medianBlur(img,5)
t5 = cv2.bilateralFilter(img,9,75,75)

titles =['Original','Averaged','Simple blur','Gaussian blur','Median blur','Bilateral filter']
imgs = [img,t1,t2,t3,t4,t5]

for i in range(6) :
    plt.subplot(2,3,i+1),plt.imshow(imgs[i]),plt.title(titles[i])
plt.show()