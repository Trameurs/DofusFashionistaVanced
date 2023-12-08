export PYTHONPATH=$PYTHONPATH:~/DofusFashionistaVanced
cd ~/DofusFashionistaVanced
bash -c './wipe_solution_cache.py'
cd fashionsite
bash -c 'django-admin compilemessages'
cd ..
export DJANGO_SETTINGS_MODULE=fashionsite.settings
gunicorn fashionsite.wsgi:application --bind 0.0.0.0:8000