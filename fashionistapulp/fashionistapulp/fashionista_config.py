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

import os
import platform

path = None

def get_fashionista_path():
    global path
    if path is None:
        system_type = platform.system()
        config_file_path = ''
        if system_type == 'Windows':
            config_file_path = os.path.join(os.environ['APPDATA'], 'fashionista', 'config')
        elif system_type == 'Linux':
            config_file_path = '/etc/fashionista/config'

        with open(config_file_path) as f:
            path = f.read().strip()
    return path

def get_items_db_path():
    return os.path.join(get_fashionista_path(), 'fashionistapulp', 'fashionistapulp', 'items.db')

def get_items_dump_path():
    return os.path.join(get_fashionista_path(), 'fashionistapulp', 'fashionistapulp', 'item_db_dumped.dump')

def load_items_db_from_dump():
    run_root_script('load_item_db.py')

def save_items_db_to_dump():
    run_root_script('dump_item_db.py')

def run_root_script(script_path):
    ENV_VAR = 'PYTHONPATH=%s' % (os.path.join(get_fashionista_path(), 'fashionistapulp'))
    LOAD_SCRIPT_PATH = os.path.join(get_fashionista_path(), script_path)
    os.system('%s %s' % (ENV_VAR, LOAD_SCRIPT_PATH))

serve_static = None

def serve_static_files():
    global serve_static
    if serve_static is None:
        system_type = platform.system()
        serve_static_file_path = ''
        if system_type == 'Windows':
            serve_static_file_path = os.path.join(os.environ['APPDATA'], 'fashionista', 'serve_static')
        elif system_type == 'Linux':
            serve_static_file_path = '/etc/fashionista/serve_static'

        with open(serve_static_file_path) as f:
            serve_static = f.read().startswith('True')
    return serve_static