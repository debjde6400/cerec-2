import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

t = 0.01
l_r = 0.0001

c = np.array([1.0, 1.0])

xs = np.array([[2], [5], [7], [10], [12]], dtype=np.float32)
ys = np.array([[30], [32], [28], [45], [70]], dtype=np.float32)

#print(xs[:,1])

def gradient_descent(c, xs, ys, thresold, l_r):
  n = len(xs)
  copy_c = c.copy()
  xs = np.hstack((np.ones((n,1)), xs.reshape(-1,1)))
  cost_function = lambda x: ( 1.0 / n) * np.sum((np.matmul(x, c.T) - ys) ** 2)

  ct1 = cost_function(xs)
  #print(ct1)
  ct2 = ct1 + 100.0
  i = 0

  while(abs(ct2 - ct1) > thresold):
    i += 1
    c[0] = c[0] - (l_r / n) * np.sum(np.matmul(xs, c.T) - ys)
    c[1] = c[1] - (l_r / n) * np.sum((np.matmul(xs, c.T) - ys) * xs[:,1])
    ct2 = ct1
    ct1 = cost_function(xs)
    if i % 10 == 0:
      print("Iteration : {} :: {}, {}\n".format(i, ct1, ct2))
      print("ct2 - ct1 : {}".format(abs(ct2 - ct1)))

    if i == 150:
      print('Current learning rate reaches limit of iteration, trying with slower rate. \nParameters changed to original ones and process restarts.\n **\n')
      i = 0
      l_r = l_r / 10
      c = copy_c.copy()
      print(c)
      ct1 = cost_function(xs)
      ct2 = ct1 + 100.0
      print(ct1)

  print("Final Iteration : {} :: {}, {}\n".format(i, ct1, ct2))
  return c

def plot_data(c, xs, ys):
  plt.scatter(xs, ys, s=2.0)
  plt.plot(xs, np.matmul(np.hstack((np.ones((len(xs),1)), np.array(xs).reshape(-1,1))), c.transpose()), c='r')
  plt.show()

#coef = gradient_descent(c, xs, ys, t, l_r)
#plot_data(coef, xs, ys)

data = pd.read_csv("D:/CSV files and Datasets/archive/train.csv")
#print(data)
data.dropna(subset=['y'], inplace=True)

X = data['x']
y = data['y']

coef = gradient_descent(c, X.to_numpy(), y.to_numpy(), t, l_r)
print(coef)
plot_data(coef, X, y)