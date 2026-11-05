from datetime import (date, timedelta)
#import urllib3
import json
import requests
#import ssl_verify

#http = urllib3.PoolManager()

headers = {"User-Agent": "PostmanRuntime/7.30.1"}


def es_habil(d: date = date.today()) -> bool:
    if d.weekday() > 4:
        return False

    url = f"https://apis.digital.gob.cl/fl/feriados/{d.year}/{d.month}/{d.day}"

    #r = http.request("GET", url, headers=headers, verify=False)

    r =requests.get(url, headers=headers,verify=False)
    data=r.content
    #print(data)

    if "error" in json.loads(data):
        return True

    return False


def previo(d: date = date.today()) -> date:
    delta = timedelta(days=1)

    d -= delta
    while not es_habil(d):
        d -= delta

    return d
