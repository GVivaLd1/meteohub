import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from main.models import WeatherReport

sys.stdout.reconfigure(encoding='utf-8')

weather_map = {
    "Безхмарно": "clear",
    "Хмарно, дощ, гроза": "storm",
    "Хмарно, сильний дощ, гроза": "storm",
    "Малохмарно, дощ, гроза": "storm",
    "Хмарно, невеликий дощ": "sunny_rain",
    "Малохмарно, невеликий дощ": "sunny_rain",
    "Малохмарно, дощ": "sunny_rain",
    "Хмарно, дощ": "rain",
    "Похмуро, дощ": "rain",
    "Малохмарно": "little_clouds",
    "Хмарно, без істотних опадів": "little_clouds",
    "Похмуро": "clouds",
    "Хмарно": "clouds",
    "Малохмарно, град": "hailstorm",
    "Хмарно, невеликий дощ, гроза": "little_rain",
    "Похмуро, невеликий дощ": "little_rain"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def parse_meteofor(city_obj):
    url = f"https://meteofor.com.ua/weather-{city_obj.url_name}-4944/weekly/"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    weekly_forecast = soup.find("div", class_="widget-body")

    if not weekly_forecast:
        print(f"[-] Парсер meteofor не знайшов блок прогнозу для міста {city_obj.name}")
        return
    
    temperatures_row = weekly_forecast.find("div", class_="values")
    temperatures = temperatures_row.find_all("div", class_="value")
    icons = weekly_forecast.find_all("div", class_="row-item")

    today_date = date.today()
    
    for i in range(0, 7):
        time.sleep(3)
        target_date = today_date + timedelta(days=i)

        min_str = temperatures[i].find("div", class_="mint").find("temperature-value").get("value")
        max_str = temperatures[i].find("div", class_="maxt").find("temperature-value").get("value")

        min_temp = int(min_str)
        max_temp = int(max_str)

        weather_string = icons[i].get("data-tooltip")

        report, created = WeatherReport.objects.update_or_create(
            city=city_obj,
            source="Meteofor",
            target_date=target_date,
            
            defaults={
                "min_temp": min_temp,
                "max_temp": max_temp,
                "condition": weather_map[weather_string]
            }
        )

        status = "Створено" if created else "Оновлено"
        print(f"[{status}] {city_obj.name} | {target_date} | Мін: {min_temp}°C | Макс: {max_temp}°C - Meteofor")