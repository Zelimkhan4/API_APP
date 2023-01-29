import sys
from PIL import Image
from io import BytesIO
import requests


def calculate_span(obj):
    l1, r1 = map(float, obj["boundedBy"]["Envelope"]["lowerCorner"].split())
    l2, r2 = map(float, obj["boundedBy"]["Envelope"]["upperCorner"].split())
    return f"{abs(l1 - l2) / 2},{abs(r1 - r2) / 2}"


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

    static_map_server = "http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": coords,
        "l": "map",
        "spn": calculate_span(f_object),
        "pt": f"{coords},pm2rdl"
    }

    response = requests.get(static_map_server, params=params)
    Image.open(BytesIO(response.content)).show()
else:
    print(f"Объект по адресу: {obj} не найден!")