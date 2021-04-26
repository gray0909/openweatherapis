from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    lat = models.CharField(max_length=10)
    long = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    temp = models.FloatField(null=False)
    condition = models.CharField(max_length=20)
