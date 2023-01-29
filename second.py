from utils import get_nearest_pharmacy, get_distance
import requests
import sys
from PIL import Image
from io import BytesIO


obj = "".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": obj,
    "format": "json"
}


response = requests.get(geocoder_api_server, params=params)
json_response = response.json()
objects = json_response["response"]["GeoObjectCollection"]['featureMember']
if objects:
    f_object = objects[0]["GeoObject"]
    coords = ",".join(f_object["Point"]["pos"].split())

    pharmacy = get_nearest_pharmacy(coords)
    if pharmacy is None:
        pos = coords
    pos = pharmacy["geometry"]["coordinates"]


    static_map_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        "l": "map",
        "pt": f"{coords},pm2rdl~{pos[0]},{pos[1]},pm2rdl"
    }

    response = requests.get(static_map_server, params=params)
    distance = get_distance(coords, f"{pos[0]},{pos[1]}")
    metaData = pharmacy["properties"]["CompanyMetaData"]
    address = metaData.get("address", None)
    time = metaData.get("Hours", dict()).get("text", None)
    name = metaData.get("name", None)
    print(f"{name}\n{address}\n{time}\nРасстояние - {round(distance)} метров")
    Image.open(BytesIO(response.content)).show()
else:
    print(f"Объект по адресу: '{obj}' не найден!")



