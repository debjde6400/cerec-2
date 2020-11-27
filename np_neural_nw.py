import numpy as np

# N : batch size, H : hidden dimension, D_* : input and output dimensions
N, D_in, H, D_out = 64, 1000, 100, 10

# Data
x = np.random.randn(N, D_in)
print(x[:2,:2], '\n')
print(x.shape, '\n')
y = np.random.randn(N, D_out)
print(y[:2,:2], '\n')
print(y.shape, '\n')

# initial weights
w1 = np.random.randn(D_in, H)
print(w1[:2,:2], '\n')
print(w1.shape, '\n')
w2 = np.random.randn(H, D_out)
print(w2[:2,:2], '\n')
print(w2.shape, '\n')

learning_rate = 1e-6

for t in range(2):
  # Forward pass : compute predicted y
  h = x.dot(w1)    # h : hypothesis, here we apply weight w1 on x (input data)
  print(h[:2,:2], '\n')
  print(h.shape, '\n')
  h_relu = np.maximum(h, 0)  # sigmoid function (activation function), converts computed value into something closer to target value
  print(h_relu[:2,:2], '\n')
  print(h.shape, '\n')
  y_pred = h_relu.dot(w2)  # next layer calculation where result of 1st layer is processed with w2

  # Compute and print loss
  loss = np.square(y_pred - y)
  print(t, loss[:2,:2])

  # Backprop to compute gradients of w1 and w2 w.r.t loss
  grad_y_pred = 2.0 * (y_pred - y)
  grad_w2 = h_relu.T.dot(grad_y_pred)
  grad_h_relu = grad_y_pred.dot(w2.T)
  grad_h = grad_h_relu.copy()
  grad_h[h < 0] = 0
  grad_w1 = x.T.dot(grad_h)

  # Update weights
  w1 -= learning_rate * grad_w1
  w2 -= learning_rate * grad_w2

print(w1[:2, :2], '\n', w2[:2, :2])