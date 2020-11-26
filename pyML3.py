import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import pandas as pd

df = pd.read_csv('datasets/breast-cancer-wisconsin.data')
df.replace('?',-99999,inplace=True)
df.drop(['id'],1,inplace=True)

X = np.array(df.drop(['class'],1))
y = np.array(df['class'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = neighbors.KNeighborsClassifier()
clf.fit(X_train, y_train)

acc = clf.score(X_test, y_test)
print(acc)

example_m = np.array([4,2,1,1,1,2,3,2,1]).reshape(1,-1)
pred = clf.predict(example_m)
print(pred)