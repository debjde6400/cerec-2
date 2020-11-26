# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 22:13:43 2019

@author: Debanjan Dey
"""

import pandas as pd
import numpy as np

dt = pd.read_csv("D:/Python programs/datasets/breast-cancer-wisconsin.csv")
print(dt.head())

dt1 = dt[:5]
dt2 = dt[5:10]

print(np.linalg.eig(dt2))