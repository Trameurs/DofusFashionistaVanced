import os
import sys

with open('/etc/fashionista/config') as f:
    path = f.read()

sys.path.append(path + '/fashionistapulp')
sys.path.append(path + '/fashionsite')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fashionsite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
