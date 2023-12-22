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

items_with_extralines = []
for item in data:
    if 'special_spell_en' in item:
        item_info = {
            'name': item['name_en'],
            'special_spell': item['special_spell_en']
        }
        items_with_extralines.append(item_info)

with open('items_with_extralines.json', 'w', encoding='utf-8') as file:
    json.dump(items_with_extralines, file, ensure_ascii=False, indent=4)
