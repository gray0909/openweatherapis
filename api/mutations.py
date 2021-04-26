import graphene
from .models import City, Weather
from .types import CityType, CityInput, WeatherType, WeatherInput


class CreateCity(graphene.Mutation):
    class Arguments:
        city_data = CityInput(required=True)

    city = graphene.Field(CityType)

    @staticmethod
    def mutate(root, info, city_data=None):
        city_instance = City(
            name=city_data.name,
            lat=city_data.lat,
            long=city_data.long
        )
        city_instance.save()
        return CreateCity(city=city_instance)


class UpdateCity(graphene.Mutation):
    class Arguments:
        city_data = CityInput(required=True)

    city = graphene.Field(CityType)

    @staticmethod
    def mutate(root, info, city_data=None):

        city_instance = City.objects.get(pk=city_data.id)

        if city_instance:
            city_instance.name = city_data.name
            city_instance.lat = city_data.lat
            city_instance.long = city_data.long

            return UpdateCity(city=city_instance)
        return UpdateCity(city=None)


class DeleteCity(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    city = graphene.Field(CityType)

    @staticmethod
    def mutate(root, info, id):
        city_instance = City.objects.get(pk=id)
        city_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_city = CreateCity.Field()
    update_city = UpdateCity.Field()
    delete_city = DeleteCity.Field()