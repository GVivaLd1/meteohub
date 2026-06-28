import time
from datetime import date
from django.core.management.base import BaseCommand
from main.models import City
from main.models import WeatherReport
from main.parsers.sinoptic import parse_sinoptic
from main.parsers.meteofor import parse_meteofor
from main.parsers.pogoda_radar import parse_pogoda_radar

class Command(BaseCommand):
    help = "Запускає процес парсингу погоди з джерел. Оновлює БД додаючи/оновлюючи актуальні прогнози та видаляючи застарілі"

    def handle(self, *args, **options):
        WeatherReport.objects.filter(target_date__lt=date.today()).delete()
        active_cities = City.objects.filter(is_monitored=True)

        if not active_cities:
            return
        
        for city in active_cities:
            try:
                parse_sinoptic(city)
                parse_meteofor(city)
                parse_pogoda_radar(city)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\nПомилка парсингу: {e}"))

            time.sleep(2)

        self.stdout.write(self.style.SUCCESS('\nПарсинг успішно завершено!'))