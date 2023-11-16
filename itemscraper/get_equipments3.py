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
from fashionistapulp.dofus_constants import STAT_NAME_TO_KEY, STAT_ORDER, TYPE_NAME_TO_SLOT

# Read the original JSON file
with open('transformed_items.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

with open('transformed_sets.json', 'r', encoding='utf-8') as f:
    original_sets = json.load(f)

# Open the .dump file for writing
with open('item_db_dumped.dump', 'w', encoding='utf-8') as f:
    # Write initial SQL commands
    f.write("PRAGMA foreign_keys=OFF;\nBEGIN TRANSACTION;\nCREATE TABLE item_types\n             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text);\n")

    # Write item_types INSERT commands
    for index, item in enumerate(TYPE_NAME_TO_SLOT, start=1):
        f.write(f"INSERT INTO item_types VALUES ({index},'{item}');\n")

    # Write CREATE TABLE for stats
    f.write("CREATE TABLE stats\n             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text,\n             key text);\n")

    # Write stats INSERT commands
    for index, item in enumerate(STAT_NAME_TO_KEY, start=1):
        f.write(f"INSERT INTO stats VALUES({index},'{item}','{STAT_NAME_TO_KEY[item]}');\n")

    # Write CREATE TABLE for stats_of_items
    #f.write("CREATE TABLE stats_of_items\n             (item INTEGER, stat INTEGER, value INTEGER,\n             FOREIGN KEY(item) REFERENCES items(id),\n             FOREIGN KEY(stat) REFERENCES stats(id));\n")

    # Write CREATE TABLE for sets
    f.write("""CREATE TABLE "sets" (
	    `id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	    `name`	text,
	    `ankama_id`	INTEGER,
	    `dofustouch`	INTEGER
    );\n""")

    #INSERT INTO sets VALUES(1,'Pink Piwi Set',70,NULL);

    for index, item in enumerate(original_sets["sets"], start=1):
        f.write(f"INSERT INTO sets VALUES({index},'{item['name']}',{item['ankama_id']},NULL);\n")

    # Write CREATE TABLE for items
    f.write("""CREATE TABLE "items" (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` text,
        `level` INTEGER,
        `type` INTEGER,
        `item_set` INTEGER,
        `ankama_id` INTEGER,
        `ankama_type` text,
        `removed` INTEGER,
        `dofustouch` INTEGER,
        FOREIGN KEY(`type`) REFERENCES item_types (id),
        FOREIGN KEY(`item_set`) REFERENCES sets (id)
    );\n""")

    #INSERT INTO items VALUES(6854,'Leurnettes',12,1,NULL,340,'equipment',0,1);
    
    for index, item in enumerate(original_data, start=1):
        # Write INSERT command for items
        if item['w_type'] == 'Trophy':
            item['w_type'] = 'Dofus'
        if item['w_type'] == 'Prysmaradite':
            item['w_type'] = 'Dofus'
        if item['w_type'] == 'Backpack':
            item['w_type'] = 'Cloak'
        if item['w_type'] == 'Petsmount':
            item['w_type'] = 'Pet'

        if item['w_type'] not in TYPE_NAME_TO_SLOT:
            item['w_type'] = 'Weapon'

        set_id = None
        
        for i, set in enumerate(original_sets['sets'], start=1):
            if item['ankama_id'] in set['equipment_ids']:
                set_id = i  # Using the index as the set ID
                break

        # Use 'NULL' if set_id is None, otherwise use the set_id
        set_id_or_null = 'NULL' if set_id is None else set_id
        
        f.write(f"INSERT INTO items VALUES({index},'{item['name']}',{item['level']},{list(TYPE_NAME_TO_SLOT.values()).index(item['w_type'].lower()) + 1},{set_id_or_null},{item['ankama_id']},{item['ankama_type']},NULL,NULL);\n")

        # Write INSERT commands for stats_of_items
        #for stat in item['stats']:
        #    f.write(f"INSERT INTO stats_of_items VALUES({item['id']},{stat['stat']},{stat['value']});\n")