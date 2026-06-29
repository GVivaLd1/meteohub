from django.db import models

class City(models.Model):
    name = models.CharField(verbose_name="Назва міста", max_length=50, unique=True)
    url_name = models.CharField(verbose_name="URL-назва", max_length=50, unique=True, null=True)
    is_monitored = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
class WeatherReport(models.Model):
    weather_coditions = [
        ('clear', 'Ясно'),
        ('clear_night', 'Ясно, ніч'),
        ('little_clouds', 'Малохмарно'),
        ('clouds', 'Хмарно'),
        ('clouds_night', 'Хмарно, ніч'),
        ('gloom', 'Похмуро'), 
        ('little_rain', 'Невеликий дощ'),
        ('rain', 'Дощ'),
        ('sunny_rain', 'Дощ з сонцем'),
        ('snow', 'Сніг'),
        ('light_snow', 'Невеликий сніг'),
        ('snow_and_rain', 'Сніг з дощем'),
        ('storm', 'Гроза'),
        ('hailstorm', 'Град')
    ]

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_reports')

    source = models.CharField(verbose_name="Джерело", max_length=50)
    min_temp = models.IntegerField(verbose_name="Мін. температура", null=True)
    max_temp = models.IntegerField(verbose_name="Макс. температура", null=True)
    parsed_at = models.DateTimeField(verbose_name="Час парсингу", auto_now_add=True, null=True)
    target_date = models.DateField(verbose_name="Дата прогнозу", null=True)
    condition = models.CharField(verbose_name="Стан погоди", max_length=20, choices=weather_coditions, null=True)

    @property
    def icon_path(self):
        if not self.condition:
            return "main/img/weather_icons/not_found.png"
        return f"main/img/weather_icons/{self.condition}.png"

    class Meta:
        unique_together = ['city', 'source', 'target_date']
        verbose_name = "Прогноз погоди"
        verbose_name_plural = "Прогнози погоди"

    def __str__(self):
        return f"{self.city.name} | {self.min_temp}°C - {self.max_temp}°C | {self.source} | {self.parsed_at}"