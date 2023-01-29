import requests


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