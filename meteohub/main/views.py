from datetime import date, timedelta
from django.shortcuts import render
from .models import City, WeatherReport
from django.db.models import Count

def index(request):
    city = City.objects.first()
    
    today = date.today()
    target_dates = [today + timedelta(days=i) for i in range(7)]
    
    reports = WeatherReport.objects.filter(city=city, target_date__in=target_dates)

    # Групування звітів за джерелами
    grouped_data = {}
    
    for report in reports:
        source = report.source
        
        if source not in grouped_data:
            grouped_data[source] = {d: None for d in target_dates}
            
        grouped_data[source][report.target_date] = report

    # Отримання часу останнього парсингу
    last_report = WeatherReport.objects.order_by("-parsed_at").first()

    last_update_time = last_report.parsed_at if last_report else None

    # Збирання загальної статистики
    general_statistics = {}

    lowest_temp_report = reports.order_by("min_temp").first()
    highest_temp_report = reports.order_by("-max_temp").first()

    if lowest_temp_report and highest_temp_report:
        general_statistics["lowest_temp"] = [lowest_temp_report.min_temp, lowest_temp_report.source]
        general_statistics["highest_temp"] = [highest_temp_report.max_temp, highest_temp_report.source]
    else:
        general_statistics["lowest_temp"] = None
        general_statistics["highest_temp"] = None

    general_condition_stats = list(reports.values("condition").annotate(total=Count("condition")).order_by("-total"))

    if general_condition_stats:
        # Отримання найрідкісніших погодних умов
        min_count = general_condition_stats[-1]["total"]

        least_frequent_conditions_codes = [
            item["condition"] for item in general_condition_stats if item["total"] == min_count
        ]
        LFC_readable_names = [
            WeatherReport(condition=code).get_condition_display() for code in least_frequent_conditions_codes
        ]
        
        final_LFC_string = " / ".join(LFC_readable_names)

        # Отримання найчастіших погодних умов
        max_count = general_condition_stats[0]["total"]

        most_frequent_conditions_codes = [
            item["condition"] for item in general_condition_stats if item["total"] == max_count
        ]
        MFC_readable_names = [
            WeatherReport(condition=code).get_condition_display() for code in most_frequent_conditions_codes
        ]
        
        final_MFC_string = " / ".join(MFC_readable_names)

        general_statistics["least_frequent_condition"] = final_LFC_string
        general_statistics["most_frequent_condition"] = final_MFC_string

    else:
        general_statistics["least_frequent_condition"] = "Немає даних"
        general_statistics["most_frequent_condition"] = "Немає даних"

    # Створення поденної погодної статистики
    days_statistics = {}

    for t_date in target_dates:
        date_key = t_date.strftime("%d.%m")

        if date_key not in days_statistics:
            days_statistics[date_key] = {}

        t_date_reports = WeatherReport.objects.filter(city=city, target_date=t_date)

        lowest_temp_report = t_date_reports.order_by("min_temp").first()
        highest_temp_report = t_date_reports.order_by("-max_temp").first()
            
        if lowest_temp_report and highest_temp_report:
            days_statistics[date_key]["lowest_temp"] = [lowest_temp_report.min_temp, lowest_temp_report.source]
            days_statistics[date_key]["highest_temp"] = [highest_temp_report.max_temp, highest_temp_report.source]
        else:
            days_statistics[date_key]["lowest_temp"] = None
            days_statistics[date_key]["highest_temp"] = None

        condition_stats = list(t_date_reports.values("condition").annotate(total=Count("condition")).order_by("-total"))

        if condition_stats:
            # Отримання найрідкісніших погодних умов
            min_count = condition_stats[-1]["total"]

            least_frequent_conditions_codes = [
                item["condition"] for item in condition_stats if item["total"] == min_count
            ]
            LFC_readable_names = [
                WeatherReport(condition=code).get_condition_display() for code in least_frequent_conditions_codes
            ]
            
            final_LFC_string = " / ".join(LFC_readable_names)

            # Отримання найчастіших погодних умов
            max_count = condition_stats[0]["total"]
    
            most_frequent_conditions_codes = [
                item["condition"] for item in condition_stats if item["total"] == max_count
            ]
            MFC_readable_names = [
                WeatherReport(condition=code).get_condition_display() for code in most_frequent_conditions_codes
            ]
            
            final_MFC_string = " / ".join(MFC_readable_names)

            days_statistics[date_key]["least_frequent_condition"] = final_LFC_string
            days_statistics[date_key]["most_frequent_condition"] = final_MFC_string

        else:
            days_statistics[date_key]["least_frequent_condition"] = "Немає даних"
            days_statistics[date_key]["most_frequent_condition"] = "Немає даних"

    forecast = {
        "city": city,
        "dates": target_dates,
        "grouped_data": grouped_data,
        "last_update_time": last_update_time,
        "general_statistics": general_statistics,
        "days_statistics": days_statistics
    }
    return render(request, "main/index.html", forecast)
