from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    city = "Tokyo"
    weather_info = {"city": city, "temp": None, "error": None}

    if request.method == "POST":
        city = request.form.get("city")

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_data = requests.get(geo_url).json()

    if "results" in geo_data and len(geo_data["results"]) > 0:
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # 2. Weather API: Fetch the live temperature for those coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url).json()

        weather_info["city"] = city.title()
        weather_info["temp"] = weather_data["current_weather"]["temperature"]
    else:
        weather_info["error"] = "City not found. Please try again."

    return render_template("weather.html", weather=weather_info)


if __name__ == "__main__":
    # We run this on port 5001 so it doesn't collide with your existing database app
    app.run(debug=True, port=5001)
