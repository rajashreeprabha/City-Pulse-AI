import sqlite3
import joblib
import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "..", "model", "citypulse_model.pkl")

model = joblib.load(MODEL_PATH)
def predict_area(area_name):
    DB_PATH = os.path.join(BASE, "database.db")
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT fever, humidity, rain, aqi FROM city_data WHERE area=? ORDER BY timestamp DESC LIMIT 50",
        (area_name,)
    )
    rows = cursor.fetchall()
    conn.close()

    if len(rows) == 0:
        return "No Data"

    avg_data = np.mean(rows, axis=0)
    prediction = model.predict([avg_data])[0]

    return "High Risk" if prediction == 1 else "Low Risk"


# test
if __name__ == "__main__":
    print(predict_area("Anna Nagar"))
