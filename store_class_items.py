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

import json
import sqlite3

from fashionistapulp.fashionista_config import (get_items_db_path, load_items_db_from_dump,
                                                save_items_db_to_dump) 
from store_rosetta import get_item_id_and_name_for_ankama_profile
from fashionistapulp.structure import get_structure
from fashionistapulp.item import Item
from fashionistapulp.dofus_constants import WEIRD_CONDITIONS
from fashionistapulp.modify_items_db import update_item, delete_item
from fashionistapulp.translation import NON_EN_LANGUAGES
from distutils.command.config import LANG_EXT


def main(json_file):
    weapons = read_id_to_terms(json_file)
    
    load_items_db_from_dump()
    for weapon in weapons:
        ankama_profile = (weapon['ankama_id'], 'equipment')
        
        conn = sqlite3.connect(get_items_db_path())
        c = conn.cursor()
        item_id, weapon_name = get_item_id_and_name_for_ankama_profile(c, 'items', ankama_profile)
        conn.close()
        #print item_id
        if item_id is not None:
            store_weapon_data(item_id, weapon_name, weapon)

    save_items_db_to_dump()

def store_weapon_data(item_id, weapon_name, weapon_data):
    s = get_structure()
    if 'removed' in weapon_data:
        delete_item(item_id)
    else:
        new_item = Item()
        old_item = s.get_item_by_id(item_id)
        
        new_item.id = old_item.id
        new_item.name = old_item.name
        new_item.or_name = old_item.or_name
        new_item.type = old_item.type
        new_item.level = old_item.level
        new_item.set = old_item.set
        new_item.ankama_id = old_item.ankama_id
        new_item.ankama_type = old_item.ankama_type
        new_item.stats = old_item.stats
        new_item.min_stats_to_equip = old_item.min_stats_to_equip 
        new_item.max_stats_to_equip = old_item.max_stats_to_equip   
        for lang in NON_EN_LANGUAGES:
            new_item.localized_names[lang] = old_item.localized_names.get(lang)
            
        for lang in NON_EN_LANGUAGES:
            new_item.localized_extras[lang] = old_item.localized_extras.get(lang)
        new_item.localized_extras['en'] = old_item.localized_extras.get('en')
        
        
        for wc in WEIRD_CONDITIONS:
            new_item.weird_conditions[wc] = old_item.weird_conditions[wc]
        
        new_item = _convert_json_item_to_item(weapon_data, new_item, s)
        
        if '(' in old_item.name:
            new_item.name = old_item.name
        
        print 'Checking %s' % new_item.name
        
        update_item(old_item, new_item, None, False)
    
    



def _convert_json_item_to_item(json_item, new_item, s):
    structure = s
    
    item = new_item
    for lang in json_item['extra_lines']:
        if lang == 'en':
            item.name = json_item['name']
            if json_item['w_type'] == 'Trophy':
                json_item['w_type'] = 'Dofus'
            if json_item['w_type'] == 'Backpack':
                json_item['w_type'] = 'Cloak'
            if json_item['w_type'] == 'Petsmount':
                json_item['w_type'] = 'Pet'
            item_type = structure.get_type_id_by_name(json_item['w_type'])
            if item_type:
                item.type = item_type
            else:
                item.type = structure.get_type_id_by_name('Weapon')
    item.ankama_id = json_item['ankama_id']
    item.ankama_type = 'equipment'
    item.level = json_item['level'] 
    
    for lang in json_item['extra_lines']:
        lines = []
        for line in json_item['extra_lines'][lang]:
            lines.append(line)

        item.localized_extras[lang] = lines
    return item
    
    
def read_id_to_terms(filename):
    weapons = []
    with open(filename) as f:
        weapon_list = json.load(f)
        for entry in weapon_list:
            weapons.append(entry)
    return weapons

if __name__ == '__main__':
    main('itemscraper/newitems.json')
