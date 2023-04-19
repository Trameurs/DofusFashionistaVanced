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

import datetime
import hashlib
import os
import sys

from fashionistapulp.fashionista_config import get_items_dump_path

sys.path.append('fashionsite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashionsite.settings')

import django
django.setup()

from chardata.models import SolutionMemory, ItemDbVersion

def main():
    should_wipe, new_dump_hash = check_saved_dump_hash()
    if should_wipe:
        wipe()
        save_dump_hash(new_dump_hash)

def check_saved_dump_hash():
    print_with_time('Hashing item db dump...')
    with open(get_items_dump_path(), 'rb') as f:
        current_dump_hash = hashlib.md5(f.read()).hexdigest()
        print_with_time('Item db dump is %s' % current_dump_hash)
    
    try:
        saved_db_version = ItemDbVersion.objects.latest(field_name='id')
    except ItemDbVersion.DoesNotExist:
        print_with_time('Last used db dump is null, wiping just to make sure.')
        return True, current_dump_hash

    print('Last used db dump is %s' % saved_db_version.dump_hash)
    print('That version was first used on %s' % saved_db_version.created_time)
    if saved_db_version.dump_hash != current_dump_hash:
        print('Hashes do not match, wiping.')
        return True, current_dump_hash
    else:
        print('Hashes match, leaving solution cache alone.')
        return False, current_dump_hash

def wipe():
    print_with_time('Will now wipe solution cache.')
    
    all_rows = SolutionMemory.objects.all()
    print_with_time('Solution cache held %d entries.' % all_rows.count())
    print_with_time('Deleting...')
    all_rows.delete()
    all_rows = SolutionMemory.objects.all()
    print_with_time('Finished deleting.')
    print_with_time('Solution cache now holds %d entries.' % all_rows.count())

def save_dump_hash(dump_hash):
    print_with_time('Updating last used db dump hash.')
    item_db_version = ItemDbVersion()
    item_db_version.dump_hash = dump_hash
    item_db_version.save()
    print_with_time('Done.')

def print_with_time(s):
    print '[%s] %s' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s)

if __name__ == '__main__':
    main()
