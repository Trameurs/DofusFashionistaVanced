#!/bin/bash

while true
do
    cd ~/DofusFashionistaVanced
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    export PYTHONPATH=$PYTHONPATH:/home/ec2-user/DofusFashionistaVanced/fashionsite
    export PYTHONPATH=$PYTHONPATH:/home/ec2-user/DofusFashionistaVanced
    bash -c './wipe_solution_cache.py'
    cd fashionsite
    bash -c 'django-admin compilemessages'
    cd ..
    gunicorn fashionsite.wsgi:application --bind 0.0.0.0:8000

    echo "Server crashed with exit code $?.  Respawning.." >&2
    sleep 1
done