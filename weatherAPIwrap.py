import requests
import os

headers = {
    'x-rapidapi-host': os.environ["x-rapidapi-host"],
    'x-rapidapi-key': os.environ["x-rapidapi-key"]
}

iconurl = "https://openweathermap.org/img/wn/{0}@2x.png"


def weather(inlinemessage):
    currentweatherurl = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"lat": inlinemessage.location.latitude, "lon": inlinemessage.location.longitude, "lang": "ru",
                   "units": "metric"}
    return requests.request("GET", currentweatherurl, headers=headers, params=querystring)


def weatherbycity(city):
    currentweatherurl = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"q": city, "lang": "ru",
                   "units": "metric"}
    return requests.request("GET", currentweatherurl, headers=headers, params=querystring)


def weatherbycityforecast5day(city, threehourscnt):
    currentweatherurl = "https://community-open-weather-map.p.rapidapi.com/forecast"
    querystring = {"q": city, "lang": "ru",
                   "units": "metric", "cnt": threehourscnt}
    return requests.request("GET", currentweatherurl, headers=headers, params=querystring)
