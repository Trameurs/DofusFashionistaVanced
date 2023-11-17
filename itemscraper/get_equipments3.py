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


WEAPON_TYPES = {
    'Hammer': 'hammer',
    'Axe': 'axe',
    'Shovel': 'shovel',
    'Staff': 'staff',
    'Sword': 'sword',
    'Dagger': 'dagger',
    'Bow': 'bow',
    'Wand': 'wand',
    'Pickaxe': 'pickaxe',
    'Scythe': 'scythe',
    'Lance': 'lance',
}

def escape_single_quotes(s):
    return s.replace("'", "''")

# Read the original JSON file
with open('transformed_items.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

with open('transformed_sets.json', 'r', encoding='utf-8') as f:
    original_sets = json.load(f)

# Open the .dump file for writing
with open('../fashionistapulp/fashionistapulp/item_db_dumped.dump', 'w', encoding='utf-8') as f:
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

    for index, item in enumerate(original_sets, start=1):
        f.write(f"INSERT INTO sets VALUES({index},'{escape_single_quotes(item['name'])}',{item['ankama_id']},NULL);\n")

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
            item['weapon_type'] = item['w_type']
            item['w_type'] = 'Weapon'

        set_id = None
        
        for i, set in enumerate(original_sets, start=1):
            if item['ankama_id'] in set['equipment_ids']:
                set_id = i  # Using the index as the set ID
                break

        # Use 'NULL' if set_id is None, otherwise use the set_id
        set_id_or_null = 'NULL' if set_id is None else set_id
        
        f.write(f"INSERT INTO items VALUES({index},'{escape_single_quotes(item['name'])}',{item['level']},{list(TYPE_NAME_TO_SLOT.values()).index(item['w_type'].lower()) + 1},{set_id_or_null},{item['ankama_id']},'{item['ankama_type']}',NULL,NULL);\n")

    # Write CREATE TABLE for stats_of_items
    f.write("""CREATE TABLE stats_of_item
            (item INTEGER, stat INTEGER, value INTEGER,
            FOREIGN KEY(item) REFERENCES items(id),
            FOREIGN KEY(stat) REFERENCES stats(id));\n""")

    # Write INSERT commands for stats_of_items
    for index, item in enumerate(original_data, start=1):
        for stat in item['stats']:
            if stat[2] not in STAT_NAME_TO_KEY:
                continue
            stat_value = stat[1] if stat[1] is not None else stat[0]
            f.write(f"INSERT INTO stats_of_item VALUES({index},{list(STAT_NAME_TO_KEY).index(stat[2]) + 1},{stat_value});\n")

    # Write CREATE TABLE for set_bonus
    f.write("""CREATE TABLE set_bonus
             (item_set INTEGER, num_pieces_used INTEGER, stat INTEGER, value INTEGER,
              FOREIGN KEY(item_set) REFERENCES sets(id),
              FOREIGN KEY(stat) REFERENCES stats(id));\n""")
    
    # Write INSERT commands for set_bonus
    for index, set in enumerate(original_sets, start=1):
        if 'stats' in set:
            for i, effects in enumerate(set['stats'], start=2):
                for bonus in effects:
                    if bonus[2] not in STAT_NAME_TO_KEY:
                        continue
                    f.write(f"INSERT INTO set_bonus VALUES({index},{i},{bonus[0]},{list(STAT_NAME_TO_KEY).index(bonus[2]) + 1});\n")

    # Write CREATE TABLE for min_stat_to_equip
    f.write("""CREATE TABLE min_stat_to_equip
             (item INTEGER, stat INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id),
              FOREIGN KEY(stat) REFERENCES stats(id));\n""")
    
    # Write INSERT commands for min_stat_to_equip
    for index, item in enumerate(original_data, start=1):
        if 'conditions' in item:
            for condition_string in item['conditions']:
                parts = condition_string.split(' ')  # Split the string by spaces
                if len(parts) == 3 and parts[0] in STAT_NAME_TO_KEY:
                    stat_name = parts[0]  # The stat name, e.g., "Strength"
                    operator = parts[1]  # The operator, e.g., ">"
                    stat_value = parts[2]  # The value, e.g., "34"
                    stat_index = list(STAT_NAME_TO_KEY).index(stat_name) + 1
                    if operator == '>':
                        f.write(f"INSERT INTO min_stat_to_equip VALUES({index},{stat_index},{int(stat_value)+1});\n")

    # Write CREATE TABLE for max_stat_to_equip
    f.write("""CREATE TABLE max_stat_to_equip
             (item INTEGER, stat INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id),
              FOREIGN KEY(stat) REFERENCES stats(id));\n""")
    
    # Write INSERT commands for max_stat_to_equip
    for index, item in enumerate(original_data, start=1):
        if 'conditions' in item:
            for condition_string in item['conditions']:
                parts = condition_string.split(' ')  # Split the string by spaces
                if len(parts) == 3 and parts[0] in STAT_NAME_TO_KEY:
                    stat_name = parts[0]  # The stat name, e.g., "Strength"
                    operator = parts[1]
                    stat_value = parts[2]  # The value, e.g., "34"
                    stat_index = list(STAT_NAME_TO_KEY).index(stat_name) + 1
                    if operator == '<':
                        f.write(f"INSERT INTO max_stat_to_equip VALUES({index},{stat_index},{int(stat_value)-1});\n")

    # Write CREATE TABLE for min_rank_to_equip
    f.write("""CREATE TABLE min_rank_to_equip
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id));\n""")
    
    f.write("""CREATE TABLE min_align_level_to_equip
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id));\n""")
    
    f.write("""CREATE TABLE min_prof_level_to_equip
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id));\n""")
    
    f.write("""CREATE TABLE weapon_is_onehanded
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id));\n""")
    
    f.write("""CREATE TABLE weapon_crit_hits
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id));\n""")
    
    for index, item in enumerate(original_data, start=1):
        if 'crit_chance' in item:
            f.write(f"INSERT INTO weapon_crit_hits VALUES({index},{item['crit_chance']});\n")

    f.write("""CREATE TABLE weapon_crit_bonus
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id));\n""")
    
    for index, item in enumerate(original_data, start=1):
        if 'crit_bonus' in item:
            f.write(f"INSERT INTO weapon_crit_bonus VALUES({index},{item['crit_bonus']});\n")

    f.write("""CREATE TABLE weapon_ap
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id));\n""")
    
    for index, item in enumerate(original_data, start=1):
        if 'ap' in item:
            f.write(f"INSERT INTO weapon_ap VALUES({index},{item['ap']});\n")

    f.write("""CREATE TABLE weapontype
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, key text);\n""")
    
    for index, item in enumerate(WEAPON_TYPES, start=1):
        f.write(f"INSERT INTO weapontype VALUES({index},'{item}','{WEAPON_TYPES[item]}');\n")

    f.write("""CREATE TABLE weapon_weapontype
             (item INTEGER, weapontype INTEGER,
              FOREIGN KEY(item) REFERENCES items(id),
              FOREIGN KEY(weapontype) REFERENCES weapontype(id));\n""")
    
    for index, item in enumerate(original_data, start=1):
        if 'weapon_type' in item:
            if item['weapon_type'] in WEAPON_TYPES:
                f.write(f"INSERT INTO weapon_weapontype VALUES({index},{list(WEAPON_TYPES).index(item['weapon_type']) + 1});\n")

    f.write("""CREATE TABLE weapon_hits
             (item INTEGER, hit INTEGER, min_value INTEGER, max_value INTEGER, steals INTEGER,
              heals INTEGER, element text,
              FOREIGN KEY(item) REFERENCES items(id));\n""")
    
    for index, item in enumerate(original_data, start=1):
        if 'stats' in item:
            for stat in item['stats']:
                # Extract values and description
                min_value, max_value, description = stat

                # Check if the description is a hit stat
                if description.startswith("(") and description.endswith(")"):
                    # Remove parentheses from the description
                    stat_description = description[1:-1].lower()

                    element = stat_description.split(' ')[0].lower()
                    damage_type = stat_description.split(' ')[1]

                    steals = 0
                    heals = 0

                    if damage_type == 'steal':
                        steals = 1
                    elif damage_type == 'healing':
                        heals = 1

                    if element == 'neutral':
                        element = 'neut'

                    f.write(f"INSERT INTO weapon_hits VALUES({index},{item['uses_per_turn']},{min_value},{max_value},{steals},{heals},'{element}');\n")

    f.write("""CREATE TABLE extra_lines (item INTEGER, line text, language text, FOREIGN KEY(item) REFERENCES items(id));\n""")

    #todo: add extra lines

    f.write("""CREATE TABLE item_names (item INTEGER, language text, name text, FOREIGN KEY(item) REFERENCES items(id));\n""")

    #todo: add item names

    f.write("""CREATE TABLE set_names (item_set INTEGER, language text, name text, FOREIGN KEY(item_set) REFERENCES sets(id));\n""")

    #todo: add set names

    f.write("""CREATE TABLE item_weird_conditions (item INTEGER, condition_id INTEGER, FOREIGN KEY(item) REFERENCES items(id));\n""")

    f.write(f"""DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('item_types',{len(TYPE_NAME_TO_SLOT)});
INSERT INTO sqlite_sequence VALUES('stats',{len(STAT_NAME_TO_KEY)});
INSERT INTO sqlite_sequence VALUES('weapontype',{len(WEAPON_TYPES)});
INSERT INTO sqlite_sequence VALUES('items',{len(original_data)});
INSERT INTO sqlite_sequence VALUES('sets',{len(original_sets)});
COMMIT;\n""")
    
