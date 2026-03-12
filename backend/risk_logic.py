def calculate_risk(fever, humidity, rain, aqi):
    fever = float(fever)
    humidity = float(humidity)
    rain = float(rain)
    aqi = float(aqi)

    score = (fever * 0.4) + (aqi * 0.4) + (humidity * 0.1) + (rain * 10)

    if score > 100:
        score = 100

    if score < 35:
        level = "LOW"
    elif score < 70:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return round(score, 2), level

