import pytz
import requests
from django.utils.dateparse import parse_date
from datetime import datetime
from weather_api.settings import OPEN_WEATHER_BASE_URL, OPEN_WEATHER_API_KEY
from .models import City, Weather


tz = pytz.timezone("Canada/Eastern")


def convert_unixtime_to_date(seconds):
    return parse_date(str(datetime.fromtimestamp(seconds, tz)).split(' ')[0])


def calculate_average_temp(temp_dict):
    return (temp_dict['min'] + temp_dict['max'])/2


class WeatherRestClient:

    def get_forcast_request(self, lat, long):

        url = '/data/2.5/onecall?lat={}&lon={}&appid='.format(lat, long)
        url = OPEN_WEATHER_BASE_URL+url+OPEN_WEATHER_API_KEY

        try:
            return requests.get(url=url)
        except TimeoutError:
            print("request timeout for: "+url)
        except Exception:
            print("Exception occured")

    def save_response_json(self, json_result, city):

        try:
            new_weather_list = list()
            current_weather = Weather(
                city=city,
                date=convert_unixtime_to_date(json_result['current']['dt']),
                temp=json_result['current']['temp'],
                condition=str(json_result['current']['weather'][0]['main']).strip().lower()
            )
            new_weather_list.append(current_weather)

            for weather_json in json_result['daily']:

                weather_record = Weather(
                    city=city,
                    date=convert_unixtime_to_date(weather_json['dt']),
                    temp=calculate_average_temp(weather_json['temp']),
                    condition=str(weather_json['weather'][0]['main']).strip().lower()
                )
                new_weather_list.append(weather_record)
            Weather.objects.bulk_create(new_weather_list, batch_size=7)
        except Exception as e:
            print('error loading data for city: '+city.name)

