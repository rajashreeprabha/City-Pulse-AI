import sqlite3

conn = sqlite3.connect("citypulse.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS city_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT,
    district TEXT,
    area TEXT,
    fever INTEGER,
    humidity INTEGER,
    rain INTEGER,
    aqi INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("DB ready")

