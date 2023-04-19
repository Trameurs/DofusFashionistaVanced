@echo off
set PYTHONPATH=%PYTHONPATH%;%cd%\fashionista\fashionistapulp
call wipe_solution_cache.py
cd fashionsite
call django-admin.py compilemessages
cd ..
set PYTHONPATH=%PYTHONPATH%;%cd%\fashionista\fashionistapulp
call python fashionsite\manage.py runsslserver 443
