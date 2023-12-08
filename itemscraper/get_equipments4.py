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
import requests
import os
import re

with open('transformed_equipment.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)

target_directory = '../fashionsite/staticfiles/chardata/'

for item in data:
    image_url = item.get('image_url')
    if image_url:
        # You can modify the filename as per your requirement
        if item['w_type'] == 'Petsmount' or item['w_type'] == 'Pet':
            filename = os.path.join(target_directory, "pets/", sanitize_filename(f"{item['name_en']}.png"))
        else:
            filename = os.path.join(target_directory, "items/", sanitize_filename(f"{item['name_en']}.png"))
        download_image(image_url, filename)