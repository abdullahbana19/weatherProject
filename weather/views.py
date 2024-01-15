import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=53857d1a6befffc8cef57a8827f37dde'
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            'id' : city.id 
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form, 'city': cities,}
    return render(request, 'weather/index.html', context)


def delete_city(request,pk):
    city = City.objects.get(id=pk)
    if request.method == 'POST':
        city.delete()

        return redirect('/')
    context = {'city' : city}
    return render(request,'weather/delete.html',context)