import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from main.models import WeatherReport

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def parse_pogoda_radar(city_obj):
    url = f"https://www.pogodairadar.com.ua/storinka-pohody/{city_obj.url_name}/"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    weekly_forecast = soup.find("div", class_="forecasts days wo-scrollbars")

    if not weekly_forecast:
        print(f"[-] Парсер pogodaradar не знайшов блок прогнозу для міста {city_obj.name}")
        return
    
    days_info = weekly_forecast.find_all("wo-forecast-day")[:7]

    today_date = date.today()
    
    for i, day in enumerate(days_info):
        time.sleep(3)
        target_date = today_date + timedelta(days=i)

        min_str = day.find("wo-temperature", class_="min").find("div", class_="temperature").text
        max_str = day.find("wo-temperature", class_="max").find("div", class_="temperature").text

        min_temp = int(min_str)
        max_temp = int(max_str)

        report, created = WeatherReport.objects.update_or_create(
            city=city_obj,
            source="Pogoda & Radar",
            target_date=target_date,
            
            defaults={
                "min_temp": min_temp,
                "max_temp": max_temp
            }
        )

        status = "Створено" if created else "Оновлено"
        print(f"[{status}] {city_obj.name} | {target_date} | Мін: {min_temp}°C | Макс: {max_temp}°C - Pogoda & Radar")