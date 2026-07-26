@echo off

net start "postgresql-x64-18"

cd /d E:\projects\meteohub

call .venv\Scripts\activate.bat

cd meteohub

python manage.py fetch_weather 

call venv\Scripts\deactivate.bat

net stop "postgresql-x64-18"

pause