import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from main.models import WeatherReport

sys.stdout.reconfigure(encoding='utf-8')

weather_map = {
    "Ясно": "clear",
    "Суцільна хмарність, дощ, грози": "storm",
    "Мінлива хмарність, дощ, можливі грози": "storm",
    "Суцільна хмарність, дощ": "little_rain",
    "Суцільна хмарність, дрібний дощ": "little_rain",
    "Хмарно з проясненнями, дощ": "little_rain",
    "Мінлива хмарність, дрібний дощ": "sunny_rain",
    "Мінлива хмарність, дощ": "sunny_rain",
    "Хмарно з проясненнями, дрібний дощ": "sunny_rain",
    "Суцільна хмарність, сильний дощ": "rain",
    "Невелика хмарність": "little_clouds",
    "Мінлива хмарність": "clouds",
    "Хмарно з проясненнями": "clouds",
    "Суцільна хмарність": "gloom"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def parse_sinoptic(city_obj):
    url = f"https://sinoptik.ua/pohoda/{city_obj.url_name}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    weekly_forecast = soup.find("div", class_="DMP0kolW")

    if not weekly_forecast:
        print(f"[-] Парсер sinoptic не знайшов блок прогнозу для міста {city_obj.name}")
        return
    
    days = weekly_forecast.find_all("a", class_="tkK415TH")

    today_date = date.today()
    
    for i, day in enumerate(days):
        time.sleep(3)
        target_date = today_date + timedelta(days=i)
        
        temperatures = day.find_all("p")

        if len(temperatures) >= 4:

            min_str = temperatures[1].text.replace('°', '').replace('+', '').replace('−', '-')
            max_str = temperatures[3].text.replace('°', '').replace('+', '').replace('−', '-')
            
            min_temp = int(min_str)
            max_temp = int(max_str)

            weather_string = day.find("div", class_="+STyqv+a").find("div").get("aria-label").replace("\n", " ")
            weather_code = weather_map.get(weather_string)
            
            if not weather_code:

                with open("main/management/exceptions.txt", "a", encoding="utf-8") as file:
                    file.write(f"[Sinoptik] - {weather_string} ({target_date})\n")
                continue
            
            report, created = WeatherReport.objects.update_or_create(
                city=city_obj,
                source="Sinoptik",
                target_date=target_date,
                
                defaults={
                    "min_temp": min_temp,
                    "max_temp": max_temp,
                    "condition": weather_map[weather_string]
                }
            )

            status = "Створено" if created else "Оновлено"
            print(f"[{status}] {city_obj.name} | {target_date} | Мін: {min_temp}°C | Макс: {max_temp}°C - Sinoptic")