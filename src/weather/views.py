from django.shortcuts import render
import requests

from .models import City
from .forms import CityForm
from src.helper_class.reader_csv_file import ReaderCsvFile


def index(request):
    city_name = 'Wrocław'
    key = ReaderCsvFile.read_csv_file(0, 1)

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            city_name = form.cleaned_data['name']

    form = CityForm()

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={key}'
    current_conditions = requests.get(url).json()

    city_weather = {
        "city": current_conditions['name'],
        "temperature": current_conditions['main']['temp'],
        'description': current_conditions['weather'][0]['description'],
        "icon": current_conditions['weather'][0]['icon'],
    }

    context = {'city_weather': city_weather, 'form': form}
    return render(request, 'index.html', context)
