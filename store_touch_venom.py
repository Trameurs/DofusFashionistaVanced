#!/usr/bin/env python
# coding=utf-8

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
from fashionistapulp.structure import get_structure
from fashionistapulp.item import Item
from fashionistapulp.weapon import Weapon
from fashionistapulp.dofus_constants import (ELEMENT_NAME_TO_KEY, DamageDigest,
    WEIRD_CONDITIONS)
from fashionistapulp.modify_items_db import update_item, fake_delete_item,\
    insert_item
from fashionistapulp.translation import NON_EN_LANGUAGES


def main(json_file):
    weapons = read_id_to_terms(json_file)
    
    load_items_db_from_dump()
    for ankama_id, weapon_data in weapons.iteritems():
        ankama_profile = (ankama_id, 'mounts')
        conn = sqlite3.connect(get_items_db_path())
        c = conn.cursor()
        item_id, weapon_name = get_item_id_and_name_for_ankama_profile(c, 'items', ankama_profile, True)
        conn.close()
        #print item_id
        store_weapon_data(item_id, weapon_name, weapon_data)

    save_items_db_to_dump()

def store_weapon_data(item_id, weapon_name, weapon_data):
    if item_id:
        if 'removed' in weapon_data:
            fake_delete_item(item_id, True)
        else:
            new_item, new_weapon = _convert_json_item_to_item(weapon_data)
            old_item = get_structure().get_item_by_id(item_id)
            if old_item.name == 'Gelano (#1)':
                return
            print 'Checking %s' % new_item.name
            if '(' in old_item.name:
                new_item.name = old_item.name
            new_item.ankama_type = old_item.ankama_type
                
            new_item.set = old_item.set
                
            new_item.type = old_item.type
            
            for wc in WEIRD_CONDITIONS:
                new_item.weird_conditions[wc] = old_item.weird_conditions[wc]
            
            new_item.min_stats_to_equip = old_item.min_stats_to_equip 
            new_item.max_stats_to_equip = old_item.max_stats_to_equip
                
            for lang in NON_EN_LANGUAGES:
                new_item.localized_names[lang] = old_item.localized_names.get(lang)
                
            new_item.localized_extras = old_item.localized_extras
            
            #new_item.is_one_handed = old_item.is_one_handed
            
            update_item(old_item, new_item, new_weapon, False)


    else:
        new_item, new_weapon = _convert_json_item_to_item(weapon_data)
        if new_item:
            print 'Adding %s' % new_item.name
            
            insert_item(new_item, new_weapon)
        else:
            print 'Could not insert item' 
    
    
    #===========================================================================
    # store_weapon_data_field(c, item_id, weapon_name, weapon_data,
    #                         'weapon_crit_hits', 'crit_chance')
    # store_weapon_data_field(c, item_id, weapon_name, weapon_data,
    #                         'weapon_crit_bonus', 'crit_bonus')
    # store_weapon_data_field(c, item_id, weapon_name, weapon_data,
    #                         'weapon_ap', 'ap')
    #===========================================================================
    
def store_weapon_data_field(c, item_id, weapon_name, weapon_data, table, weapon_data_field):
    new_value = weapon_data.get(weapon_data_field)
    if new_value is None:
        print 'Warning: weapon [%d] %s does not have %s' % (item_id, weapon_name, weapon_data_field)
        return

    c.execute('SELECT value FROM %s WHERE item = ?' % table,
              (item_id,))
    query_result = c.fetchone()
    if query_result is None:
        c.execute('INSERT INTO %s VALUES (?, ?)' % table,
                  (item_id, new_value))
        print ('Added weapon [%d] %s %s as %s'
               % (item_id, weapon_name, weapon_data_field, new_value))
    else:
        if query_result[0] != new_value:
            c.execute('UPDATE %s SET value = ? WHERE item = ?' % table,
                      (new_value, item_id))
            print ('Changed weapon [%d] %s %s from %s to %s'
                   % (item_id, weapon_name, weapon_data_field, query_result[0], new_value))



def get_item_id_and_name_for_ankama_profile(c, entities_table, ankama_profile, touch=False):
    if ankama_profile[1] == 'set':
        c.execute('SELECT id, name FROM %s WHERE ankama_id = ?' % entities_table,
                  (ankama_profile[0],))
    else:
        if touch:
            c.execute('SELECT id, name FROM %s WHERE ankama_id = ? AND ankama_type = ? and dofustouch = ?' % entities_table,
                      (ankama_profile[0], ankama_profile[1], 1))
        else:
            c.execute('SELECT id, name FROM %s WHERE ankama_id = ? AND ankama_type = ? and dofustouch IS NULL' % entities_table,
                      (ankama_profile[0], ankama_profile[1]))
    query_result = c.fetchone()
    if query_result is not None:
        return query_result[0], query_result[1]
    else:
        return None, None

def _convert_json_item_to_item(json_item):
    structure = get_structure()

    item = Item()
    item.removed = False
    item.name = json_item['name']
    item.ankama_id = json_item['ankama_id']
    item.ankama_type = 'equipment'
    item.level = json_item['level']
    item.dofus_touch = 1 if json_item['dofustouch'] else 0
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
    
    weapon = None
    if item.type == structure.get_type_id_by_name('Weapon'):
        weapon = Weapon()
        print item.name
        weapon.ap = int(json_item['ap'])
        weapon.crit_chance = int(json_item['crit_chance'])
        weapon.crit_bonus = int(json_item.get('crit_bonus')) if json_item.get('crit_bonus') else None
        wtype = structure.get_weapon_type_by_name(json_item['w_type'])
        if wtype:
            weapon.weapon_type = wtype.id
        else: 
            print 'COULD NOT FIND TYPE: %s' % json_item['w_type']
            return None, None
    
    
    index = 0
    for stat in json_item['stats']:
        if stat[2].startswith('('):
            hit_name = stat[2].strip('()')
            hit_element = hit_name.split()[0]
            hit_type = hit_name.split()[1]
            if hit_name != 'Hunting weapon':
                element = (ELEMENT_NAME_TO_KEY[hit_element] if hit_element != 'HP' 
                                                            else ELEMENT_NAME_TO_KEY['Fire'])
                if weapon == None:
                    weapon = Weapon()
                weapon.hits_dict[index] = DamageDigest((stat[0]), 
                                                       (stat[1] if stat[1] else stat[0]), 
                                                       element, 
                                                       True if hit_type == 'steal' else False,
                                                       False if hit_element != 'HP' else True)
                index = index + 1
        elif (stat[0] or stat[1]):
            if structure.get_stat_by_name(stat[2]):
                if stat[1] == None:
                    stat_value = stat[0]
                else:
                    if stat[0] >= 0:
                        stat_value = stat[1]
                    else:
                        stat_value = stat[0]
                _add_to_old_stat(item, structure.get_stat_by_name(stat[2]).id, stat_value)
            else:
                filetomod = open('HPitems.txt','a') 
 
                filetomod.write(item.name + ': ' + stat[2] + '\n') 
                 
                print 'COULD NOT FIND STAT %s' % stat[2]
    
                filetomod.close() 
    return item, weapon

def _add_to_old_stat(old_item, stat_id, value):
    old_item.stats.append((stat_id, value))

def read_id_to_terms(filename):
    weapons = {}
    with open(filename) as f:
        weapon_list = json.load(f)
        for entry in weapon_list:
            weapons[entry['ankama_id']] = entry
    return weapons

if __name__ == '__main__':
    main('itemscraper/dofustouch2pets.json')
