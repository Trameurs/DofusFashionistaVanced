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

path = None

def get_fashionista_path():
    global path
    if path is None:
        with open('/etc/fashionista/config') as f:
            path = f.read().strip()
    return path

# TODO: Use this in structure and manage db.
def get_items_db_path():
    return '%s/fashionistapulp/fashionistapulp/items.db' % get_fashionista_path()

def get_items_dump_path():
    return '%s/fashionistapulp/fashionistapulp/item_db_dumped.dump' % get_fashionista_path()

def load_items_db_from_dump():
    run_root_script('load_item_db.py')

def save_items_db_to_dump():
    run_root_script('dump_item_db.py')

def run_root_script(script_path):
    ENV_VAR = 'PYTHONPATH=%s/fashionistapulp' % (get_fashionista_path())
    LOAD_SCRIPT_PATH = '%s/%s' % (get_fashionista_path(), script_path)
    os.system('%s %s' % (ENV_VAR, LOAD_SCRIPT_PATH))

serve_static = None

def serve_static_files():
    global serve_static
    if serve_static is None:
        with open('/etc/fashionista/serve_static') as f:
            serve_static = f.read().startswith('True')
    return serve_static
