#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from lxml import etree

tree = etree.parse(open("ItemsData.xml", 'r'))

import os
os.remove('items.db')

import sqlite3
conn = sqlite3.connect('items.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE sets
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text)''')
             
for sets in tree.findall("S_Sets")[0].findall("S_Sets"):
    # Insert a row of data
    c.execute("INSERT INTO sets (name) VALUES (?)", (sets.get("elem"),))         


# Create table
c.execute('''CREATE TABLE item_types
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text)''')
             
for item_type in tree.findall("S_EquipmentTypes")[0].findall("S_EquipmentTypes"):
    # Insert a row of data
    c.execute("INSERT INTO item_types (name) VALUES (?)", (item_type.get("elem"),))         


# Create table
c.execute('''CREATE TABLE items
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name text, 
              level INTEGER,
              type INTEGER,
              item_set INTEGER, 
              FOREIGN KEY(type) REFERENCES item_types(id),
              FOREIGN KEY(item_set) REFERENCES sets(id))''')
             
for item in tree.findall("S_Equipment")[0].findall("S_Equipment"):
    # Insert a row of data
    c.execute("INSERT INTO items (name) VALUES (?)", (item.get("elem"),))
    

# Create table
c.execute('''CREATE TABLE stats
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text,
              key text)''')

STAT_KEYS = \
{
    'Power': 'pow',
    'Damage': 'dam',
    'Heals': 'heals',
    'AP': 'ap',
    'MP': 'mp',
    'Critical Hits': 'ch',
    'Agility': 'agi',
    'Strength': 'str',
    'Neutral Damage': 'neutdam',
    'Earth Damage': 'earthdam',
    'Intelligence': 'int',
    'Fire Damage': 'firedam',
    'Air Damage': 'airdam',
    'Chance': 'cha',
    'Water Damage': 'waterdam',
    'Vitality': 'vit',
    'Initiative': 'init',
    'Summon': 'summon',
    'Range': 'range',
    'Wisdom': 'wis',
    'Neutral Resist': 'neutres',
    'Water Resist': 'waterres',
    'Air Resist': 'airres',
    'Fire Resist': 'fireres',
    'Earth Resist': 'earthres',
    '% Neutral Resist': 'neutresper',
    '% Air Resist': 'airresper',
    '% Fire Resist': 'fireresper',
    '% Water Resist': 'waterresper',
    '% Earth Resist': 'earthresper',
    'Neutral Resist in PVP': 'pvpneutres',
    'Water Resist in PVP': 'pvpwaterres',
    'Air Resist in PVP': 'pvpairres',
    'Fire Resist in PVP': 'pvpfireres',
    'Earth Resist in PVP': 'pvpearthres',
    '% Neutral Resist in PVP': 'pvpneutresper',
    '% Air Resist in PVP': 'pvpairresper',
    '% Fire Resist in PVP': 'pvpfireresper',
    '% Water Resist in PVP': 'pvpwaterresper',
    '% Earth Resist in PVP': 'pvpearthresper',
    'Prospecting': 'pp',
    'Pods': 'pod',
    'AP Reduction': 'apred',
    'MP Reduction': 'mpred',
    'Lock': 'lock',
    'Dodge': 'dodge',
    'Reflects': 'ref',
    'Pushback Damage': 'pshdam',
    'Trap Damage': 'trapdam',
    '% Trap Damage': 'trapdamper',
    'Critical Resist': 'crires',
    'Pushback Resist': 'pshres',
    'MP Loss Resist': 'mpres',
    'AP Loss Resist': 'apres',
    'Critical Damage': 'cridam',
    'Critical Failure': 'cf',
}

PVP_STATS = [
    'Neutral Resist in PVP',
    'Water Resist in PVP',
    'Air Resist in PVP',
    'Fire Resist in PVP',
    'Earth Resist in PVP',
    '% Neutral Resist in PVP',
    '% Air Resist in PVP',
    '% Fire Resist in PVP',
    '% Water Resist in PVP',
    '% Earth Resist in PVP',
]

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
}

for stat in tree.findall("S_Attribute")[0].findall("S_Attribute"):
    # Insert a row of data
    key = STAT_KEYS.get(stat.get("elem"), None)
    if key is None:
        print 'Stat not known: %s' % stat.get("elem")
    else:
        c.execute("INSERT INTO stats (name, key) VALUES (?, ?)",
                  (stat.get("elem"), key))
for stat in PVP_STATS:
    # Insert a row of data
    key = STAT_KEYS.get(stat, None)
    if key is None:
        print 'Stat not known: %s' % stat.get("elem")
    else:
        c.execute("INSERT INTO stats (name, key) VALUES (?, ?)",
                  (stat, key))
              
for item in tree.findall("Pe_EquipmentType")[0].findall("EQUIP"):
    c.execute('SELECT * FROM item_types WHERE name = ?', (item.get("value"),))
    typeid = c.fetchone()[0]    
    c.execute("UPDATE items SET type=? WHERE name = ?", (typeid, item.get("elem")))      

for item in tree.findall("Pe_SetFromTheEquipment")[0].findall("EQUIP"):
    c.execute('SELECT * FROM sets WHERE name = ?', (item.get("value"),))
    setid = c.fetchone()[0]    
    c.execute("UPDATE items SET item_set=? WHERE name = ?", (setid, item.get("elem"))) 

for item in tree.findall("P_EquipmentLevel")[0].findall("EQUIP"):  
    c.execute("UPDATE items SET level=? WHERE name = ?", (item.get("value"), item.get("elem")))

# Create table
c.execute('''CREATE TABLE stats_of_item
             (item INTEGER, stat INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id),
              FOREIGN KEY(stat) REFERENCES stats(id))''')


c.execute('SELECT id FROM item_types WHERE name = ?', ("Shield",))
shield = c.fetchone()[0]
for item in tree.findall("P_AttributeFromEquipment")[0].findall("EQUIP"):
    c.execute('SELECT id, type FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute('SELECT type FROM items WHERE id = ?', (itemid,))
    itemtype = c.fetchone()[0]
    for stat in item.findall("ATTR"):
        stat_name = stat.get("elem")
        if (itemtype == shield):
            stat_name = stat_name + " in PVP"
        c.execute('SELECT * FROM stats WHERE name = ?', (stat_name,))
        statid = c.fetchone()[0]
        c.execute("INSERT INTO stats_of_item (item, stat, value) VALUES (?,?,?)",
                  (itemid, statid, stat.get("value"),))      



# Create table
c.execute('''CREATE TABLE set_bonus
             (item_set INTEGER, num_pieces_used INTEGER, stat INTEGER, value INTEGER,
              FOREIGN KEY(item_set) REFERENCES sets(id),
              FOREIGN KEY(stat) REFERENCES stats(id))''')
              
for sets in tree.findall("P_SetBonus")[0].findall("EQ_SET"):
    c.execute('SELECT * FROM sets WHERE name = ?', (sets.get("elem"),))
    setid = c.fetchone()[0]
    for n_slots in sets.findall("N_SLOT"):
        for stat in n_slots.findall("ATTR"):
            c.execute('SELECT * FROM stats WHERE name = ?', (stat.get("elem"),))
            statid = c.fetchone()[0]
            c.execute('''INSERT INTO set_bonus (item_set, num_pieces_used, 
                        stat, value) VALUES (?,?,?,?)''', 
                        (setid, n_slots.get("elem"), statid, stat.get("value")))                    
              
# Create table
c.execute('''CREATE TABLE min_stat_to_equip
             (item INTEGER, stat INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id),
              FOREIGN KEY(stat) REFERENCES stats(id))''')
              
for item in tree.findall("P_MinimumAttributeToEquip")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    for stat in item.findall("ATTR"):
        c.execute('SELECT * FROM stats WHERE name = ?', (stat.get("elem"),))
        statid = c.fetchone()[0]
        c.execute("INSERT INTO min_stat_to_equip (item, stat, value) VALUES (?,?,?)",
                  (itemid, statid, stat.get("value"),))      

# Create table
c.execute('''CREATE TABLE max_stat_to_equip
             (item INTEGER, stat INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id),
              FOREIGN KEY(stat) REFERENCES stats(id))''')
              
for item in tree.findall("P_MaximumAttributeToEquip")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    for stat in item.findall("ATTR"):
        c.execute('SELECT * FROM stats WHERE name = ?', (stat.get("elem"),))
        statid = c.fetchone()[0]
        c.execute("INSERT INTO max_stat_to_equip (item, stat, value) VALUES (?,?,?)",
                  (itemid, statid, stat.get("value"),))      
 
# Create table
c.execute('''CREATE TABLE min_rank_to_equip
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id))''')
              
for item in tree.findall("P_MinimumRankToEquip")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute("INSERT INTO min_rank_to_equip (item, value) VALUES (?,?)",
              (itemid, item.get("value"),))      

# Create table
c.execute('''CREATE TABLE min_align_level_to_equip
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id))''')
              
for item in tree.findall("P_MinimumAlignLevelToEquip")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute("INSERT INTO min_align_level_to_equip (item, value) VALUES (?,?)",
              (itemid, item.get("value"),))      

            
# Create table
c.execute('''CREATE TABLE min_prof_level_to_equip
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id))''')
              
for item in tree.findall("P_MinimumProfLevelToEquip")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute("INSERT INTO min_prof_level_to_equip (item, value) VALUES (?,?)",
              (itemid, item.get("value"),))      

   
# Create table
c.execute('''CREATE TABLE weapon_is_onehanded
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id))''')
              
for item in tree.findall("P_WeaponIsOneHanded")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute("INSERT INTO weapon_is_onehanded (item, value) VALUES (?,?)",
              (itemid, item.get("value"),))      


# Create table
c.execute('''CREATE TABLE weapon_crit_hits
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id))''')
              
for item in tree.findall("P_CriticalHit")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute("INSERT INTO weapon_crit_hits (item, value) VALUES (?,?)",
              (itemid, item.get("value"),))      

# Create table
c.execute('''CREATE TABLE weapon_crit_bonus
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id))''')
              
for item in tree.findall("P_CriticalBonus")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute("INSERT INTO weapon_crit_bonus (item, value) VALUES (?,?)",
              (itemid, item.get("value"),))      

# Create table
c.execute('''CREATE TABLE weapon_ap
             (item INTEGER, value INTEGER,
              FOREIGN KEY(item) REFERENCES items(id))''')
              
for item in tree.findall("P_APtoHit")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute("INSERT INTO weapon_ap (item, value) VALUES (?,?)",
              (itemid, item.get("value"),))      

# Create table
c.execute('''CREATE TABLE weapontype
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, key text)''')
              
for stat in tree.findall("S_DEF_WeaponTypes")[0].findall("S_DEF_WeaponTypes"):
    key = WEAPON_TYPES.get(stat.get("elem"), None)
    if key is None:
        print 'Weapon type not known: %s' % stat.get("elem")
    else:
        c.execute("INSERT INTO weapontype (name, key) VALUES (?, ?)",
                  (stat.get("elem"), key))

# Weapon weapontype
c.execute('''CREATE TABLE weapon_weapontype
             (item INTEGER, weapontype INTEGER,
              FOREIGN KEY(item) REFERENCES items(id),
              FOREIGN KEY(weapontype) REFERENCES weapontype(id))''')
              
for item in tree.findall("Pe_WeaponType")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    c.execute('SELECT * FROM weapontype WHERE name = ?', (item.get("value"),))
    weapontype = c.fetchone()[0]
    c.execute("INSERT INTO weapon_weapontype (item, weapontype) VALUES (?,?)",
              (itemid, weapontype,))

# Weapon hits
c.execute('''CREATE TABLE weapon_hits
             (item INTEGER, hit INTEGER, min_value INTEGER, max_value INTEGER, steals INTEGER,
              heals INTEGER, element text,
              FOREIGN KEY(item) REFERENCES items(id))''')

ELEMENT_NAME_TO_KEY = {
    'Neutral': 'neut',
    'Earth': 'earth',
    'Fire': 'fire',
    'Water': 'water',
    'Air': 'air',
}

class DamageHit:
    def __init__(self):
        self.min = None
        self.max = None
        self.steals = False
        self.heals = False
        self.element = None
        
    def __repr__(self):
        return '%s%s-%s %s' % ('Steals ' if self.steals else 'Heals ' if self.heals else '' ,
                            self.min, self.max, self.element)

    def steals_int(self):
        return 1 if self.steals else 0

    def heals_int(self):
        return 1 if self.heals else 0

    def element_key(self):
        return ELEMENT_NAME_TO_KEY[self.element]

damages = {}
HIT_NUMBER = {'First Hit': 0, 'Second Hit': 1, 'Third Hit': 2, 'Fourth Hit': 3, 'Fifth Hit': 4}
for item in tree.findall("P_MinDamage")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    
    hits = item.findall("HIT")
    damages[itemid] = [None] * 5
    for hit in hits:
        damages[itemid][HIT_NUMBER[hit.get("elem")]] = DamageHit()
        damages[itemid][HIT_NUMBER[hit.get("elem")]].min = int(float(hit.get("value")))

for item in tree.findall("P_MaxDamage")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    
    hits = item.findall("HIT")
    for hit in hits:
        damages[itemid][HIT_NUMBER[hit.get("elem")]].max = int(float(hit.get("value")))

for item in tree.findall("P_Steals")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    
    hits = item.findall("HIT")
    for hit in hits:
        if hit.get("value"):
            damages[itemid][HIT_NUMBER[hit.get("elem")]].steals = True

for item in tree.findall("P_Heals")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    
    hits = item.findall("HIT")
    for hit in hits:
        if hit.get("value"):
            damages[itemid][HIT_NUMBER[hit.get("elem")]].heals = True

for item in tree.findall("Pe_HitElement")[0].findall("EQUIP"):
    c.execute('SELECT * FROM items WHERE name = ?', (item.get("elem"),))
    itemid = c.fetchone()[0]
    
    hits = item.findall("HIT")
    print item.get('elem')
    for hit in hits:
        damages[itemid][HIT_NUMBER[hit.get("elem")]].element = hit.get("value")

for itemid, raw_hits in damages.iteritems():
    hits = filter(lambda x: x is not None, raw_hits)
    print '%s %s' % (itemid, str(hits))
    for i, hit in enumerate(hits):
        c.execute("INSERT INTO weapon_hits (item, hit, min_value, max_value, steals, heals, element) VALUES (?,?,?,?,?,?,?)",
                  (itemid, i, hit.min, hit.max, hit.steals_int(), hit.heals_int(),
                   hit.element_key()))
    
# Save (commit) the changes
conn.commit()

conn.close()
