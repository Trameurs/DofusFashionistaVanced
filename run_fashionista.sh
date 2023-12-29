#!/bin/bash

while true
do
    export PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp
    bash -c './wipe_solution_cache.py'
    cd fashionsite
    bash -c 'django-admin compilemessages'
    cd ..
    export PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp
    bash -c 'python fashionsite/manage.py runserver 0.0.0.0:8000'

    echo "Server crashed with exit code $?.  Respawning.." >&2
    sleep 1
done