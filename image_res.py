# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 23:49:30 2020

@author: Debanjan Dey
"""

def jpeg_res(filename):
  with open(filename, 'rb') as img_file:
    img_file.seek(18)
    #height of an image (in 2 bytes) is at 164th position
    a = img_file.read(2)
    height = (a[0] << 8) + a[1]
    a = img_file.read(2)
    width = (a[0] << 8) + a[1]
    
  print("Resolution of image is : ",width, " x ",height)
  
jpeg_res("adidas.JPG")