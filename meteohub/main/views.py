from datetime import date, timedelta
from django.shortcuts import render
from .models import City, WeatherReport

def index(request):
    city = City.objects.first()
    
    today = date.today()
    target_dates = [today + timedelta(days=i) for i in range(7)]
    
    reports = WeatherReport.objects.filter(city=city, target_date__in=target_dates)

    grouped_data = {}
    
    for report in reports:
        source = report.source
        
        if source not in grouped_data:
            grouped_data[source] = {d: None for d in target_dates}
            
        grouped_data[source][report.target_date] = report

    last_report = WeatherReport.objects.order_by('-parsed_at').first()

    last_update_time = last_report.parsed_at if last_report else None

    forecast = {
        'city': city,
        'dates': target_dates,
        'grouped_data': grouped_data,
        'last_update_time': last_update_time
    }
    return render(request, 'main/index.html', forecast)
