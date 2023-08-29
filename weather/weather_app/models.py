

from django.db import models

class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    weather_condition = models.CharField(max_length=100)
    wind_speed = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.created_at}"

