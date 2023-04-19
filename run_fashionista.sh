PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp bash -c './wipe_solution_cache.py'
cd fashionsite
bash -c 'django-admin.py compilemessages'
cd ..
PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp bash -c 'python fashionsite/manage.py runsslserver 443'


