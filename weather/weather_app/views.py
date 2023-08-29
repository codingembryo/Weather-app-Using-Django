from django.shortcuts import render

# Create your views here.

import requests
from django.shortcuts import render
from .models import WeatherData
from .forms import LocationForm

def fetch_weather_data(location):
    api_key = "5e6ee867963cbf995f4c4556b6a80fa8"
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_weather_data(data):
    if data:
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_condition = data['weather'][0]['description']
        location = data['name'] + ', ' + data['sys']['country']
        wind_speed = data['wind']['speed']

        return {
            "temperature": temperature,
            "humidity": humidity,
            "weather_condition": weather_condition,
            "location": location,
            "wind_speed": wind_speed
        }
    else:
        return None

def index(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            weather_data = fetch_weather_data(location)
            processed_data = process_weather_data(weather_data)
            if processed_data:
                WeatherData.objects.create(
                    location=location,
                    temperature=processed_data['temperature'],
                    humidity=processed_data['humidity'],
                    weather_condition=processed_data['weather_condition'],
                    wind_speed=processed_data['wind_speed']
                )
                return render(request, "weather_app/index.html", {"weather_data": processed_data})
    else:
        form = LocationForm()

    return render(request, "weather_app/index.html", {"form": form})
