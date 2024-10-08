import requests
import json

class GeocodeApi:
    def __init__(self, api_key):
        self.__base_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}"


    def __get_data(self, city):
        params = {
            "geocode": city,
            "lang": "ru_RU",
            "format": "json",
        }
        response = requests.get(self.__base_url, params=params)
        return response

    def get_cities(self, city):
        data = json.loads(self.__get_data(city).text)
        max_to_find = 5
        number_to_find = int(data["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"])
        number_of_found = 0

        cities = []
        for i in range(0, number_to_find):
            base = data["response"]["GeoObjectCollection"]["featureMember"][i]["GeoObject"]

            kind = base["metaDataProperty"]["GeocoderMetaData"]["kind"]
            if kind in ["locality", "district", "province"]:
                coords = base["Point"]["pos"]
                address = base["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"].replace("Россия, ", "")
                city = {"address": address,
                        "coords": coords.split()}
                cities.append(city)
                number_of_found += 1
            if max_to_find == number_of_found:
                break
        return cities
