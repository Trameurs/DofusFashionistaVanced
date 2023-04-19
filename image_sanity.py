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

import os
import pprint
import sys
from fashionistapulp.fashion_util import normalize_name
from fashionistapulp.structure import get_structure

def main():
    sys.stdout = open('sanity_output.txt', 'w')

    items_in_dir = {}
    for folder in ['items', 'pets']:
        images = os.listdir(
                'fashionsite/chardata/static/chardata/%s' % folder)
        items_in_dir[folder] = set(
                [image.replace('.png', '') for image in images])
                
    # Check for items in more than one folder.
    intersection = items_in_dir['items'].intersection(items_in_dir['pets'])
    print 'Intersection:'
    pprint.pprint(intersection)
    print
    
    items_with_images = items_in_dir['items'].union(items_in_dir['pets'])
    
    structure = get_structure()
    items_in_db = set([normalize_name(item.name) for item in structure.get_items_list()])
    
    # Check for items in db but not in images.
    items_in_db_without_images = items_in_db - items_with_images
    print ('items_in_db_without_images: %d items '
           % len(items_in_db_without_images))
    pprint.pprint(items_in_db_without_images)
    print
    
    # Check for items that have imags but are not in db.
    items_with_images_not_in_db = items_with_images - items_in_db
    print ('items_with_images_not_in_db: %d items '
           % len(items_with_images_not_in_db))
    pprint.pprint(items_with_images_not_in_db)
    print
    
main()
