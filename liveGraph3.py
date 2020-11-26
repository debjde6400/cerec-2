# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 23:06:50 2018

@author: User
"""

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

x = np.array([dt.datetime(2012, 10, 19, 10, 0, 0),
              dt.datetime(2012, 10, 19, 10, 0, 1),
              dt.datetime(2012, 10, 19, 10, 0, 2),
              dt.datetime(2012, 10, 19, 10, 0, 3)])

y = np.array([1, 3, 4, 2])

fig, (ax1, ax2) = plt.subplots(nrows = 2, sharex = True)
ax1.plot(x, y, 'b-')
'''ax2.plot(x, 1.0/y, 'r-')'''
plt.show()