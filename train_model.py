# train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle

# 🌱 Sample dummy dataset (replace this with real sensor data)
data = {
    'soil_moisture': [55, 35, 20, 10],
    'leaf_temp':     [25, 30, 34, 38],
    'air_temp':      [26, 32, 36, 42],
    'humidity':      [70, 50, 40, 25],
    'light':         [30000, 35000, 45000, 50000],
    'soil_ph':       [6.8, 6.5, 6.0, 5.5],
    'ec':            [1.5, 1.2, 1.0, 0.7],
    'stem_diameter': [8.5, 7.0, 6.0, 4.5],
    'leaf_thickness':[0.35, 0.30, 0.25, 0.20],
    'label':         [0, 1, 2, 3]  # 0=Healthy, 3=Severe
}

df = pd.DataFrame(data)

# 🧠 Features and labels
X = df.drop('label', axis=1)
y = df['label']

# 🎯 Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🌳 Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 📊 Evaluation
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 💾 Save model to model.pkl
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as model.pkl")  