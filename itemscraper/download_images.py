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

import json
import os
import time
import urllib.request, urllib.parse, urllib.error


JSON_TO_DIR = {
    'dofusweap2.json': 'items',
    'allitemsnew2.json': 'items',
    #'pets.json': 'pets',
    #'mounts.json': 'mounts',
}

def main():
    i = 1
    for json_file, folder_name in JSON_TO_DIR.items():
        folder = '../fashionsite/chardata/static/chardata/%s' % folder_name
        with open(json_file) as f:
            for entry in json.load(f):
                image_path = folder + '/' + entry['name'] + '.png'
                if not os.path.isfile(image_path):
                    print('[%d] Downloading %s' % (i, entry['name']))
                    urllib.request.urlretrieve(entry['image_url'],
                                       image_path)
                    time.sleep(1)
                else:
                    print('Skipping %s' % entry['name'])
                i += 1

main()
