import requests
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from main.models import City, WeatherReport

class Command(BaseCommand):
    help = "Отримує погодні дані за минулий день через Open-meteo API"

    def handle(self, *args, **kwargs):
        cities = City.objects.filter(is_monitored=True)

        if not cities:
            self.stdout.write(self.style.WARNING("Не знайдено жодного міста для моніторингу."))
            return

        today = date.today()

        for city in cities:
            self.stdout.write(f"Оновлюємо дані для міста: {city.name}...")

            url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": city.latitude,
                "longitude": city.longitude,
                "daily": ["temperature_2m_max", "temperature_2m_min"],
                "timezone": "Europe/Kyiv",
                "past_days": 1
            }

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                data = response.json() 

                daily_data = data.get('daily', {})
                dates = daily_data.get('time', [])
                max_temps = daily_data.get('temperature_2m_max', [])
                min_temps = daily_data.get('temperature_2m_min', [])

                yesterday_date = dates[0]
                yesterday_max = max_temps[0]
                yesterday_min = min_temps[0]

                WeatherReport.objects.update_or_create(
                    city=city,
                    source="Open-Meteo",
                    target_date=yesterday_date,
                    forecast_date=yesterday_date, 
                    defaults={
                        'max_temp': yesterday_max,
                        'min_temp': yesterday_min,
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Успішно оновлено {city.name}"))

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Помилка при запиті до API для {city.name}: {e}"))