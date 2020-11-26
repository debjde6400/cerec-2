# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 18:29:35 2018

@author: User
"""

from matplotlib import pyplot as plt

f = plt.figure()
ax = f.gca()
f.show()

for i in range(1):
    ax.plot(i, i, 'ko')
    f.canvas.draw()
    input('pause : press any key ...')
    plt.pause(2)
f.close()