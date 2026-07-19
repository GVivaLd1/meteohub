from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('api/weather/', views.get_weather_data, name="api_weather")
]