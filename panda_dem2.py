# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 20:13:58 2018

@author: User
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
style.use('ggplot')

df = pd.read_csv('ZILLOW-Z77006_ZRIFAH.csv')
print(df.head())

df.set_index('Date',inplace=True)

df.to_csv('ncsv1.csv')
print(df.head())

df1 = pd.read_csv('ncsv1.csv',index_col=0)

df1.columns = ['Austin_HPI']
print(df1.head(2))