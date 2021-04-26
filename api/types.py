import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import City, Weather


class WeatherType(DjangoObjectType):
    class Meta:
        model = Weather
        fields = ("id", "city", "date", "temp", "condition")


class CityType(DjangoObjectType):
    class Meta:
        model = City
        filter_fields = {
            'id': ['exact', 'in'],
            'name': ['exact', 'in']
        }
        fields = ("id", "name", "lat", "long")

    forcast = DjangoListField(WeatherType)

    def resolve_forcast(self, info):
        return Weather.objects.filter(city=self.id)


class WeatherInput(graphene.InputObjectType):
    id = graphene.ID()
    city_id = graphene.String(required=True, name="city")
    date = graphene.Date()
    temp = graphene.Float()
    condition = graphene.String()


class CityInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    lat = graphene.String()
    long = graphene.String()
