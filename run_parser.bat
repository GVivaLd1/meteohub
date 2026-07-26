@echo off

net start "postgresql-x64-18"

cd /d E:\projects\meteohub

call .venv\Scripts\activate.bat

cd meteohub

python manage.py update_forecast

call venv\Scripts\deactivate.bat

net stop "postgresql-x64-18"