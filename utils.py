import requests
import math


def get_nearest_pharmacy(ll):
    geosearch_api_server = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптеки",
        "lang": "ru_RU",
        "ll": ll,
        "type": "biz"
    }
    response = requests.get(geosearch_api_server, params=params)
    json_response = response.json()
    objects = json_response["features"]
    if objects:
        return objects[-1]
    return None


def calculate_span(obj):
    l1, r1 = map(float, obj["boundedBy"]["Envelope"]["lowerCorner"].split())
    l2, r2 = map(float, obj["boundedBy"]["Envelope"]["upperCorner"].split())
    return f"{abs(l1 - l2) / 2},{abs(r1 - r2) / 2}"


def get_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = map(float, a.split(","))
    b_lon, b_lat = map(float, b.split(","))

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance