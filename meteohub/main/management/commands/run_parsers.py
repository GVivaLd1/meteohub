import time
from django.core.management.base import BaseCommand
from main.models import City
from main.parsers.sinoptic import parse_sinoptic

class Command(BaseCommand):
    help = "Пропускає всі активні міста через ряд погодних парсерів"

    def handle(self, *args, **options):
        active_cities = City.objects.filter(is_monitored=True)

        if not active_cities:
            return
        
        for city in active_cities:
            try:
                parse_sinoptic(city)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\nПомилка парсингу: {e}"))

            time.sleep(2)

        self.stdout.write(self.style.SUCCESS('\nПарсинг успішно завершено!'))