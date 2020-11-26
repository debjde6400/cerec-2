# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 20:50:23 2018

@author: User
"""
import quandl
import pandas as pd

api_key =  'uQ6Xym8SgcypPhVHsnoF'
df = quandl.get('FMAC/HPI_ABITX',authtoken=api_key)

print(df.head())