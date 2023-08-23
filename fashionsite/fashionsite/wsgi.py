# Copyright (C) 2020 The Dofus Fashionista
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
WSGI config for fashionsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

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
