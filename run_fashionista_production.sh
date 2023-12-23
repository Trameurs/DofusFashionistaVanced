cd ~/DofusFashionistaVanced
export PYTHONPATH=$PYTHONPATH:$(pwd)
export PYTHONPATH=$PYTHONPATH:/home/ec2-user/DofusFashionistaVanced/fashionsite
export PYTHONPATH=$PYTHONPATH:/home/ec2-user/DofusFashionistaVanced
bash -c './wipe_solution_cache.py'
cd fashionsite
bash -c 'django-admin compilemessages'
python manage.py collectstatic --noinput
cd ..
gunicorn fashionsite.wsgi:application --bind 0.0.0.0:8000