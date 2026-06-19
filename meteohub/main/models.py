from django.db import models

class City(models.Model):
    name = models.CharField(verbose_name="Назва міста", max_length=100, unique=True)


    def __str__(self) -> str:
        return self.name
    
class WeatherReport(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_reports')

    source = models.CharField(verbose_name="Джерело", max_length=50)
    temperature = models.IntegerField(verbose_name="Температура")
    date_parsed = models.DateTimeField(verbose_name="Дата парсингу", auto_now_add=True)

    def __str__(self):
        return f"{self.city.name} | {self.temperature}°C | {self.source} | {self.date_parsed}"