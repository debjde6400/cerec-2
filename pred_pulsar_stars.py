import numpy as np
import matplotlib.pyplot as np
import pandas as pd
import seaborn as sns

df = pd.read_csv("./pulsar_stars/pulsar_stars.csv")

X = df.iloc[:, :8].values
y = df.iloc[:, -1].values

print(df.head())