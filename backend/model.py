import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Dummy training data (for demo)
data = {
    "fever": [20, 40, 60, 80],
    "humidity": [30, 50, 70, 90],
    "rain": [0, 0, 1, 1],
    "aqi": [50, 120, 200, 300],
    "risk": [0, 0, 1, 1]
}

df = pd.DataFrame(data)

X = df.drop("risk", axis=1)
y = df["risk"]

model = RandomForestClassifier()
model.fit(X, y)

# Save model
BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "..", "model")
os.makedirs(MODEL_PATH, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_PATH, "citypulse_model.pkl"))

print("Model trained and saved successfully")
