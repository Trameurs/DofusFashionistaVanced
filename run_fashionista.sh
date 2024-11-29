#!/bin/bash

trap 'echo "Stopping server..."; exit' INT

while true
do
    export PYTHONPATH=$PYTHONPATH:~/DofusFashionistaVanced/fashionistapulp

    ./wipe_solution_cache.py

    cd fashionsite
    django-admin compilemessages
    cd ..

    python3 fashionsite/manage.py runserver 0.0.0.0:8000

    echo "Server crashed with exit code $?. Respawning..." >&2
    sleep 1
done
