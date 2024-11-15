#!/bin/bash

while true
do
    # Set the PYTHONPATH to include necessary directories
    export PYTHONPATH=$PYTHONPATH:~/DofusFashionistaVanced/fashionistapulp

    # Run the cache-wiping script
    ./wipe_solution_cache.py

    # Compile Django translations
    cd fashionsite
    django-admin compilemessages
    cd ..

    # Run the Django development server
    python3 fashionsite/manage.py runserver 0.0.0.0:8000

    # If the server crashes, print a message and restart after 1 second
    echo "Server crashed with exit code $?. Respawning..." >&2
    sleep 1
done
