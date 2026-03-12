import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# -------------------------------
# DATABASE CONFIG
# -------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///citypulse.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------
# DATABASE MODEL
# -------------------------------
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(100))
    area = db.Column(db.String(100))
    level = db.Column(db.String(20))

# create table if not exists
with app.app_context():
    db.create_all()

# -------------------------------
# HOME (Dashboard)
# -------------------------------
@app.route("/")
def home():
    return render_template("dashboard.html")

# -------------------------------
# PUBLIC FORM PAGE
# -------------------------------
@app.route("/form")
def form():
    return render_template("public_form.html")

# -------------------------------
# SUBMIT DATA
# -------------------------------
@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json()

    district = data.get("district")
    area = data.get("area")
    fever = int(data.get("fever"))
    humidity = int(data.get("humidity"))
    aqi = int(data.get("aqi"))

    score = fever + humidity + aqi

    if score < 150:
        level = "LOW"
    elif score < 250:
        level = "MEDIUM"
    else:
        level = "HIGH"

    new_report = Report(
        district=district,
        area=area,
        level=level
    )

    db.session.add(new_report)
    db.session.commit()

    return jsonify({"message": "Report Stored"})

# -------------------------------
# DISTRICT AGGREGATION LOGIC
# -------------------------------
@app.route("/map-data")
def map_data():

    districts = db.session.query(Report.district).distinct()
    results = []

    for d in districts:
        district_name = d[0]
        reports = Report.query.filter_by(district=district_name).all()

        low = 0
        medium = 0
        high = 0

        for r in reports:
            if r.level == "LOW":
                low += 1
            elif r.level == "MEDIUM":
                medium += 1
            else:
                high += 1

        total = len(reports)

        if total == 0:
            continue

        # ✅ CONFIDENCE %
        confidence = round((max(low, medium, high) / total) * 100)

        # ✅ MINIMUM DATA LOGIC
        if total < 5:
            final_level = "INSUFFICIENT DATA"
        elif high >= medium and high >= low:
            final_level = "HIGH"
        elif medium >= low:
            final_level = "MEDIUM"
        else:
            final_level = "LOW"

        results.append({
            "district": district_name,
            "level": final_level,
            "confidence": confidence,
            "reports": total
        })

    return jsonify(results)


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
