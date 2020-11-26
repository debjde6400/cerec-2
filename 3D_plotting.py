import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dataset = pd.read_csv('june-2017.csv')
dataset = dataset[pd.notnull(dataset['140_temperature'])]

ds_X = np.array(dataset[['140_temperature', '140_humidity']])
ds_z = np.array(dataset['140_pm25'])

ds_x = np.array(dataset['140_temperature'])
ds_y = np.array(dataset['140_humidity'])

ax = plt.axes(projection='3d')
ax.scatter3D(ds_x, ds_y, ds_z, c = 'r')

plt.title('Weather conditions')
plt.xticks()
plt.yticks()