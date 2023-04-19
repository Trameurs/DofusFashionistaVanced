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
from fashionistapulp.structure import get_structure, invalidate_structure
from fashionistapulp.set import Set
from fashionistapulp.modify_items_db import update_set
from fashionistapulp.translation import NON_EN_LANGUAGES


def main(json_file):
    sets_dict = read_id_to_terms(json_file)
    
    load_items_db_from_dump()
    for ankama_id, set_data in sets_dict.iteritems():
        set_name = set_data.get('name')
        print set_name
        if set_name:
            conn = sqlite3.connect(get_items_db_path())
            c = conn.cursor()
            c.execute('SELECT id FROM %s WHERE name = ?' % 'sets', (set_name,))
            query_result = c.fetchone()
            conn.close()
            if query_result is not None:
                store_set_data(query_result[0], ankama_id, set_data)
            else:
                filetomod = open('MissingSets.txt','a') 
 
                name_to_print = set_name + '\n'
                filetomod.write(name_to_print.encode('utf-8')) 
    
                filetomod.close() 
    save_items_db_to_dump()
    invalidate_structure()

def store_set_data(item_id, ankama_id, set_data):
    if 'removed' in set_data:
        return
    else:
        new_set = _convert_json_item_to_item(set_data)
        old_set = get_structure().get_set_by_id(item_id)
        print 'Checking %s' % new_set.name

        new_set.items = old_set.items

        for lang in NON_EN_LANGUAGES:
            new_set.localized_names[lang] = old_set.localized_names.get(lang)
 
        update_set(item_id, new_set, False)

def _convert_json_item_to_item(json_set):
    structure = get_structure()
        
    my_set = Set()
    my_set.name = json_set['name']
    my_set.ankama_id = json_set['ankama_id']
    for bonus in json_set['bonus']:
        bonus_stats = json_set['bonus'][bonus]
        bonus_number = int(bonus.strip('bonus_'))
        my_set.bonus_per_num_items[bonus_number] = {}
        for stat in bonus_stats:
            stat_value = None
            if stat.startswith('Reflects'):
                stat = stat.split(' ', 2)
                stat_name = stat[0]
                stat_value = int(stat[1])
            else:
                stat = stat.split(' ', 1)
                stat_name = stat[1]
            if stat[1] == 'Physical Reduction':
                for stat_name in ('Neutral Resist', 'Earth Resist'):
                    stat_obj = structure.get_stat_by_name(stat_name)
                    if stat_obj:
                        stat_id = stat_obj.id
                        stat_name = stat_obj.name
                        stat_value = (stat_value if stat_value else int(stat[0]))
                        my_set.bonus.append((bonus_number, stat_id, stat_value))
                        my_set.bonus_per_num_items[bonus_number][stat_name] = stat_value
            else:
                stat_name = stat_name.replace('Resistance', 'Resist')
                stat_name = stat_name.replace('Critical', 'Critical Hits')
                stat_name = stat_name.replace('Critical Hits Damage', 'Critical Damage')
                stat_name = stat_name.replace('Critical Hits Resist', 'Critical Resist')
                stat_name = stat_name.replace('Power (traps)', '% Trap Damage')
                stat_name = stat_name.replace('pods', 'Pods')
                stat_name = stat_name.replace('Summons', 'Summon')
                stat_name = stat_name.replace('MP Parry', 'MP Loss Resist')
                stat_name = stat_name.replace('AP Parry', 'AP Loss Resist')
                if '%' in stat[0] and not 'Critical' in stat_name and not 'Power' in stat_name:
                    stat_name = '% ' + stat_name
                stat_obj = structure.get_stat_by_name(stat_name)
                if stat_obj:
                    stat_id = stat_obj.id
                    stat_name = stat_obj.name
                    stat_value = (stat_value if stat_value else int(stat[0].strip('%')))
                    my_set.bonus.append((bonus_number, stat_id, stat_value))
                    my_set.bonus_per_num_items[bonus_number][stat_name] = stat_value
                else:
                    print 'COULD NOT FIND %s' % stat_name
    return my_set

def read_id_to_terms(filename):
    setses = {}
    with open(filename) as f:
        weapon_list = json.load(f)
        for entry in weapon_list:
            setses[entry['ankama_id']] = entry
    return setses

if __name__ == '__main__':
    main('itemscraper/sets.json')
