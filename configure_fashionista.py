#!/usr/bin/env python

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

import getpass
import platform
import os
import json
from subprocess import call

# Determine the correct python command
PYTHON_CMD = "python3" if platform.system() != "Windows" else "python"

if platform.system() == 'Windows':
    CONFIG_DIR = os.path.join(os.environ['APPDATA'], 'fashionista\gen_config.json')
else:
    CONFIG_DIR = '/etc/fashionista'

def load_config():
    """Load the database configuration from a JSON file."""
    with open(CONFIG_DIR, 'r') as config_file:
        return json.load(config_file)

def main():
    # Load database credentials
    config = load_config()
    db_user = config.get('mysql_USER', 'root')  # Default to 'root' if not specified
    db_password = config.get('mysql_PASSWORD', '')
    db_name = 'fashionista'

    if platform.system() != 'Windows' and getpass.getuser() == 'root':
        print('Run this script as a regular user, not as root.')
        return

    _print_header('Creating database')
    call([
        'mysql',
        '-u', db_user,
        '-p' + db_password,
        '-e', f'CREATE DATABASE IF NOT EXISTS {db_name};'
    ])

    _print_header('Syncing db')
    call([PYTHON_CMD, 'fashionsite/manage.py', 'migrate'])
    call([PYTHON_CMD, 'fashionsite/manage.py', 'migrate', 'chardata'])
    
    if platform.system() != 'Windows':
        call(['chmod', '777', 'fashionsite'])

    _print_header('Done')

def _print_header(header):
    print('=' * 60)
    print(header)
    print('=' * 60)

if __name__ == '__main__':
    main()