import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def sigmoid(sc):
  return 1 / (1 + np.exp(-sc))

def logistic_regression(features, target, steps, l_r):
  intercept = np.ones((features.shape[0], 1))
  features = np.hstack((intercept, features))
  weights = np.zeros(features.shape[1])
  
  for s in range(steps):
    scores = np.dot(features, weights)
    preds = sigmoid(scores)
    
    output_error = preds - target
    grad = np.dot(features.T, output_error)
    weights -= l_r * grad
  
  return weights

pulsar_data = pd.read_csv("D:\CSV files and Datasets\pulsar_stars.csv")
pulsar_data = pulsar_data[:250]

data_X = pulsar_data.iloc[:, :-1]
data_y = pulsar_data.iloc[:, -1]

plt.bar(data_y.unique(), data_y.value_counts())
plt.xticks([0, 1])
plt.xlabel('Target class')
plt.ylabel('Counts')
plt.title('Counts of occurances of various values of target class')
plt.show()

weights = logistic_regression(data_X, data_y, 340, 0.0001)
print(weights)

data_with_intercept = np.hstack((np.ones((data_X.shape[0], 1)), data_X))
final_scr = np.dot(data_with_intercept, weights)
preds = (np.round(sigmoid(final_scr))).astype('int64')
pulsar_data['tc_by_lr'] = pd.DataFrame(preds)

plt.bar(pulsar_data['tc_by_lr'].unique(), pulsar_data['tc_by_lr'].value_counts())
plt.xticks([0, 1])
plt.xlabel('Target class')
plt.ylabel('Counts')
plt.title('Counts of occurances of various values of target class as predicted by algortihm')
plt.show()

correct_pred = pulsar_data[(pulsar_data['target_class'] == pulsar_data['tc_by_lr'])]
print('Out of {0} rows, the algorithm gave correct results for {1} rows.'
      .format(len(pulsar_data), len(correct_pred)))
correct_pred.head()

acc_p = (len(correct_pred) / len(pulsar_data)) * 100
print('Accuracy of the algorithm : {0} %'.format(acc_p))