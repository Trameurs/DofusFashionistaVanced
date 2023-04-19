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

from fashionistapulp.fashionista_config import (get_items_db_path, load_items_db_from_dump) 


def main(json_file):
    weapons = read_id_to_terms(json_file)
    
    load_items_db_from_dump()
    
    f= open("missing.txt","w+")
    f.write("[")
    for ankama_id in weapons:
        print 'Checking %d %s' % (ankama_id, weapons[ankama_id])
        ankama_profile = (ankama_id, 'equipment')
        conn = sqlite3.connect(get_items_db_path())
        c = conn.cursor()
        item_id, weapon_name = get_item_id_and_name_for_ankama_profile(c, 'items', ankama_profile)
        conn.close()
        
        if not (item_id and weapon_name):
            f.write('{"ankama_id": %d, "name": "%s"},\n' % (ankama_id, weapons[ankama_id]))
    f.close()


def get_item_id_and_name_for_ankama_profile(c, entities_table, ankama_profile, touch=False):
    if ankama_profile[1] == 'set':
        c.execute('SELECT id, name FROM %s WHERE ankama_id = ?' % entities_table,
                  (ankama_profile[0],))
        print 'a'
    else:
        if touch:
            c.execute('SELECT id, name FROM %s WHERE ankama_id = ? AND ankama_type = ? and dofustouch = ?' % entities_table,
                      (ankama_profile[0], ankama_profile[1], 1))
            print 'b'
        else:
            c.execute('SELECT id, name FROM %s WHERE ankama_id = ?' % entities_table,
                      (ankama_profile[0],))
            print 'c'
    query_result = c.fetchone()
    print query_result
    print '\n\n'
    if query_result is not None:
        return query_result[0], query_result[1]
    else:
        return None, None

def read_id_to_terms(filename):
    weapons = {}
    with open(filename) as f:
        weapon_list = json.load(f)
        for entry in weapon_list:
            weapons[entry['ankama_id']] = entry['name']
    return weapons

if __name__ == '__main__':
    main('itemscraper/dofus248general.json')
