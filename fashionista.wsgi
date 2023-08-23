import os
import sys

sys.path.append('/home/ec2-user/DofusFashionistaVanced')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fashionsite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()