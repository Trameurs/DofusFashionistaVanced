PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp bash -c './wipe_solution_cache.py'
cd fashionsite
bash -c 'django-admin compilemessages'
cd ..
PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp bash -c 'gunicorn fashionsite.wsgi:application --bind 0.0.0.0:8000'