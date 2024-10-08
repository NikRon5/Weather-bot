import requests
import json
from datetime import datetime


# Open-meteo api
class WeatherApi:
    def __init__(self, api_key):
        self.__base_url = "https://api.open-meteo.com/v1/forecast?"
        self.__headers = {"X-Gismeteo-Token": api_key}

    # Getting weather forecast for coords
    def get_current_weather(self, coords):
        if type(coords) is not list or len(coords) != 2:
            return {}
        # Current - temperature, apparent temperature, pressure, clouds
        # Hourly - temperature
        # Daily - precipitation probability
        params = {
            "longitude": coords[0],
            "latitude": coords[1],
            "timezone": "Europe/Moscow",
            "current": "temperature_2m,apparent_temperature,surface_pressure,cloud_cover",
            "hourly": "temperature_2m",
            "daily": "precipitation_probability_max",
            "forecast_days": "1"
        }
        response = requests.get(self.__base_url, headers=self.__headers, params=params)
        data = json.loads(response.text)

        if "error" in data:
            return {}

        # Current time of the forecast
        current_time = datetime.fromisoformat(data["current"]["time"])

        # Dictionary for a data of the current weather and hourly weather (temperature by hours)
        output = {"current_weather":
                      {"time": current_time.strftime("%H:%M"),
                           "temperature": round(data["current"]["temperature_2m"]),
                           "apparent_temperature": round(data["current"]["apparent_temperature"]),
                           "precipitation_probability": data["daily"]["precipitation_probability_max"][0],
                           "pressure": round(data["current"]["surface_pressure"]/1.333),
                           "cloud_cover": data["current"]["cloud_cover"]},
                  "hourly_weather": []}

        # Hours of the forecast from current time
        hourly_time = [datetime.fromisoformat(time) for time in data["hourly"]["time"] if
                       datetime.fromisoformat(time).hour >= current_time.hour]

        # Temperature by hours
        hourly_weather = data["hourly"]["temperature_2m"][hourly_time[0].hour:]

        # Adding temperature of every hour to output data
        for i in range(len(hourly_time)):
            hour_output = {"time": hourly_time[i].strftime("%H:%M"),
                    "temperature": hourly_weather[i]}
            output["hourly_weather"].append(hour_output)

        return output