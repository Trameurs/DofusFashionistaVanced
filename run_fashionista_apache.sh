PYTHONPATH=$PYTHONPATH:~/fashionista/fashionistapulp bash -c './wipe_solution_cache.py'
cd fashionsite
bash -c 'django-admin compilemessages'
sudo systemctl restart httpd

