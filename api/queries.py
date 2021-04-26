import datetime
import json
import graphene
from django.db.models import Max
from datetime import date
from .models import City, Weather
from .types import CityType, WeatherType
from .utils import WeatherRestClient


weather_client = WeatherRestClient


class Query(graphene.ObjectType):
    all_city = graphene.List(CityType)  # Use to get ID and name of preloaded cities

    visits_city = graphene.List(
        CityType,
        weather_con=graphene.String(),
        city_list=graphene.List(graphene.String),
        day_diff=graphene.Int()
    )

    hottest_city = graphene.List(
        CityType,
        city_list=graphene.List(graphene.String),
        day_diff=graphene.Int()     # Max 7 days
    )

    def resolve_all_city(self, info, **kwargs):
        return City.objects.all()

    def resolve_visits_city(self, info, weather_con, city_list=[], day_diff=0):
        if len(city_list) == 0:
            cities = City.objects.all()
        else:
            cities = City.objects.filter(name__in=city_list)

        for city in cities:
            weather = Weather.objects.filter(
                city_id=city.id,
                date=date.today() + datetime.timedelta(days=day_diff),
                condition=str(weather_con).strip().lower()
            )
            if len(weather) == 0:
                result = weather_client.get_forcast_request(self, lat=city.lat, long=city.long)
                weather_client.save_response_json(self, json.loads(result.content), city)


        weather_conditions = Weather.objects.filter(
            city__in=cities,
            date=date.today() + datetime.timedelta(days=day_diff),
            condition=str(weather_con).strip().lower()
        )

        if len(weather_conditions) != 0:
            return City.objects.filter(weather__in=weather_conditions)
        else:
            return None



    def resolve_hottest_city(self, info, city_list=[], day_diff=0):

        # open weather api must be queried with lat long, ideally would have static table of cities
        if len(city_list) == 0:
            cities = City.objects.all()
        else:
            cities = City.objects.filter(name__in=city_list)

        # cannot use bulk thus looping through each desired city
        for city in cities:
            weather = Weather.objects.filter(
                city_id=city.id,
                date=date.today() + datetime.timedelta(days=day_diff)
            )
            if len(weather) == 0:
                result = weather_client.get_forcast_request(self, lat=city.lat, long=city.long)
                weather_client.save_response_json(self, json.loads(result.content), city)

        return cities.annotate(max_temp=Max('weather__temp')).order_by('-max_temp')[:3]

