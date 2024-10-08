import requests
import json
from datetime import datetime


class WeatherApi:
    def __init__(self, api_key):
        self.__base_url = "https://api.open-meteo.com/v1/forecast?"
        self.__headers = {"X-Gismeteo-Token": api_key}

    def get_current_weather(self, coords):
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

        current_time = datetime.fromisoformat(data["current"]["time"])
        output = {"current_weather":
                      {"time": current_time.strftime("%H:%M"),
                           "temperature": round(data["current"]["temperature_2m"]),
                           "apparent_temperature": round(data["current"]["apparent_temperature"]),
                           "precipitation_probability": data["daily"]["precipitation_probability_max"][0],
                           "pressure": round(data["current"]["surface_pressure"]/1.333),
                           "cloud_cover": data["current"]["cloud_cover"]},
                  "hourly_weather": []}

        hourly_time = [datetime.fromisoformat(time) for time in data["hourly"]["time"] if
                       datetime.fromisoformat(time).hour >= current_time.hour]
        hourly_weather = data["hourly"]["temperature_2m"][hourly_time[0].hour:]

        for i in range(len(hourly_time)):
            hour_output = {"time": hourly_time[i].strftime("%H:%M"),
                    "temperature": hourly_weather[i]}
            output["hourly_weather"].append(hour_output)

        return output