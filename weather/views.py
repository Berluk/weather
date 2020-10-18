from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect

from .forms import CityForm
from helper_class.reader_csv_file import ReaderCsvFile
from helper_class.get_location import GetLocation
from helper_class.get_day import GetDay


def current_weather(url):
    forecast_conditions = requests.get(url).json()
    current_weather = {}

    for key, item in forecast_conditions['current'].items():
        if key == 'dt':
            current_day = GetDay.convert_utc_time(item)[0]
        if key == 'temp':
            current_temp = round(item)
        if key == 'weather':
            for key, item in item[0].items():
                if key == 'description':
                    current_desc = item
                if key == 'icon':
                    current_icon = item
                    current_weather.update({
                        'current_day': {
                            'day': current_day,
                            'current_temp': current_temp,
                            'current_desc': current_desc,
                            'current_icon': current_icon,
                        }
                    })

    return current_weather


def forecast_weather(url):
    forecast_conditions = requests.get(url).json()
    forecast_weather = {}

    for daily in forecast_conditions['daily']:
        days = GetDay.convert_utc_time(daily['dt'])[0]
        for key, item in daily['weather'][0].items():
            if key == 'icon':
                icon = item
            if key == 'description':
                desc = item
        for key, item in daily['temp'].items():
            if key == 'day':
                day_temp = round(item)
            if key == 'min':
                min_temp = round(item)
            if key == 'max':
                max_temp = round(item)
                forecast_weather.update({
                    days: {
                        'icon': icon,
                        'description': desc,
                        'day_temp': day_temp,
                        'max_temp': max_temp,
                        'min_temp': min_temp,
                    }
                })
    return forecast_weather


def index(request):
    key = ReaderCsvFile.read_csv_file(0, 1)
    err_msg: bool = False
    message = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            city_name = form.cleaned_data['name']
            coord = GetLocation().get_location_by_city_name(city_name)
            if coord:
                print(True)
            else:
                coord = GetLocation().get_location_by_ip_address()
                current_location = f'https://api.openweathermap.org/data/2.5/weather?lat={coord[0]}&lon={coord[1]}&units=metric&appid={key}'
                city_name = requests.get(current_location).json()['name']
                err_msg = True

        if err_msg:
            message = 'City does not exist in the world'

        form = CityForm()

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={coord[0]}&lon={coord[1]}&exclude=hourly,minutely&units=metric&appid={key}'
        current_city_weather = {
            'city': city_name
        }
        context = {
            'city_weather': current_city_weather,
            'current_weather': current_weather(url),
            'forecast': forecast_weather(url),
            'form': form,
            'message': message
        }

    else:
        coord = GetLocation().get_location_by_ip_address()
        current_location = f'https://api.openweathermap.org/data/2.5/weather?lat={coord[0]}&lon={coord[1]}&units=metric&appid={key}'
        forecast_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={coord[0]}&lon={coord[1]}&exclude=hourly,minutely&units=metric&appid={key}'

        city_name = requests.get(current_location).json()

        form = CityForm()

        current_city_weather = {
            'city': city_name['name']
        }

        context = {
            'city_weather': current_city_weather,
            'current_weather': current_weather(forecast_url),
            'forecast': forecast_weather(forecast_url),
            'form': form}

    return render(request, 'index.html', context)