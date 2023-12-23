PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp bash -c './wipe_solution_cache.py'
cd fashionsite
bash -c 'django-admin compilemessages'
python manage.py collectstatic --noinput
cd ..
PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp bash -c 'python fashionsite/manage.py runserver 0.0.0.0:8000'