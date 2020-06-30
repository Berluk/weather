import requests
from geopy import Nominatim


class GetLocation:
    locator = Nominatim(user_agent='my_application')

    def get_location_by_ip_address(self):
        url = 'http://ipinfo.io/json'
        ip_address = requests.get(url)

        location = self.locator.geocode(ip_address.json()['loc'])
        latitude = location.latitude
        longitude = location.longitude

        return latitude, longitude

    def get_location_by_city_name(self, city_name):
        location = self.locator.geocode(city_name)

        if location is not None:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return False
