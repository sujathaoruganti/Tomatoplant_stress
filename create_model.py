import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Sample training data
data = {
    'val1': [0.4, 0.6, 0.7, 0.9],
    'val2': [0.3, 0.5, 0.6, 0.8],
    'val3': [0.5, 0.7, 0.8, 1.0],
    'val4': [0.2, 0.4, 0.6, 0.7],
    'val5': [0.3, 0.5, 0.7, 0.9],
    'val6': [0.4, 0.6, 0.9, 1.1],
    'val7': [0.2, 0.5, 0.8, 1.0],
    'val8': [0.3, 0.6, 0.9, 1.2],
    'val9': [0.4, 0.7, 1.0, 1.3],
    'stress': [0, 1, 2, 3]  # 0=Healthy, 1=Mild, etc.
}

df = pd.DataFrame(data)
X = df.drop('stress', axis=1)
y = df['stress']

model = RandomForestClassifier()
model.fit(X, y)

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ model.pkl created successfully")
