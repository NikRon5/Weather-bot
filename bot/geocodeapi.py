import requests
import json


# Yandex geocode api
class GeocodeApi:
    def __init__(self, api_key):
        self.__base_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}"

    # Getting data of cities
    def __get_data(self, city):
        params = {
            "geocode": city,
            "lang": "ru_RU",
            "format": "json",
        }
        response = requests.get(self.__base_url, params=params)
        return response

    # Parsing and returning addresses and coords for founded cities
    def get_cities(self, city):
        # Got data to json
        data = json.loads(self.__get_data(city).text)

        # Max cities to get
        max_to_find = 5

        # Number of founded cities
        number_of_founded = int(data["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"])
        number_of_got = 0

        cities = []
        for i in range(0, number_of_founded):
            base = data["response"]["GeoObjectCollection"]["featureMember"][i]["GeoObject"]

            # Only "locality", "district", "province" kinds are proper
            kind = base["metaDataProperty"]["GeocoderMetaData"]["kind"]
            if kind in ["locality", "district", "province"]:
                # Getting coords and address
                coords = base["Point"]["pos"]
                address = base["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"].replace("Россия, ", "")

                # Creating dict for a city and adding it to a list
                city = {"address": address,
                        "coords": coords.split()}
                cities.append(city)
                number_of_got += 1
            if max_to_find == number_of_got:
                break
        return cities
