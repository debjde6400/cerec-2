# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 23:07:26 2020

@author: Debanjan Dey
"""

punctuations = '''!()-[]{};:'",<>./?@#$%^&*_~'''

my_str = input("Enter some string: ")

no_punct = ""

for char in my_str:
  if char not in punctuations:
    no_punct = no_punct + char
    
print(no_punct)