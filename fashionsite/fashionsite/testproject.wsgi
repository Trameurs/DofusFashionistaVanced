import os
import sys

with open('/etc/fashionista/config') as f:
    path = f.read().strip()  # using strip() to remove any leading/trailing whitespace

sys.path.append(path)  # Adding the main project directory to sys.path
sys.path.append('/home/ec2-user/DofusFashionistaVanced')
sys.path.append('/home/ec2-user/DofusFashionistaVanced/fashionistapulp')
sys.path.append('/home/ec2-user/.local/lib/python3.9/site-packages')
sys.path.append('/usr/local/lib/python3.9/site-packages')
sys.path.append(os.path.join(path, 'fashionistapulp'))
sys.path.append(os.path.join(path, 'fashionsite'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'fashionsite.settings' 

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
