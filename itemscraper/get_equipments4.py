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
current_directory = os.path.dirname(__file__)
target_directory = os.path.join(current_directory, '../fashionsite/staticfiles/chardata/')

total = len(data)
count = 0
last_percentage = -1
print(f"Total images to download: {total}")
for item in data:
    image_url = item.get('image_url')
    if image_url:
        original_name = f"{item['name_en']}.png"
        sanitized_name = sanitize_filename(original_name)

        if item['w_type'] == 'Petsmount' or item['w_type'] == 'Pet':
            directory = os.path.join(target_directory, "pets/")
        else:
            directory = os.path.join(target_directory, "items/")
        
        filename = os.path.join(directory, sanitized_name)
        
        if original_name != sanitized_name:
            print(f"Filename modified: {original_name} -> {sanitized_name}")
        
        download_image(image_url, filename)
        
        count += 1
        percentage = int((count / total) * 100)
        if percentage > last_percentage:
            print(f"Progress: {percentage}%")
            last_percentage = percentage