from django.db import models

class City(models.Model):
    name = models.CharField(verbose_name="Назва міста", max_length=50, unique=True)
    url_name = models.CharField(verbose_name="URL-назва", max_length=50, unique=True, null=True)
    is_monitored = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
class WeatherReport(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_reports')

    source = models.CharField(verbose_name="Джерело", max_length=50)
    min_temp = models.IntegerField(verbose_name="Мін. температура", null=True)
    max_temp = models.IntegerField(verbose_name="Макс. температура", null=True)
    parsed_at = models.DateTimeField(verbose_name="Час парсингу", auto_now_add=True, null=True)
    target_date = models.DateField(verbose_name="Дата прогнозу", null=True)

    class Meta:
        unique_together = ['city', 'source', 'target_date']
        verbose_name = "Прогноз погоди"
        verbose_name_plural = "Прогнози погоди"

    def __str__(self):
        return f"{self.city.name} | {self.min_temp}°C - {self.max_temp}°C | {self.source} | {self.parsed_at}"