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

STAT_TRANSLATE = {
    '% Power': 'Power',
    'Damage': 'Damage',
    'Heals': 'Heals',
    'AP': 'AP',
    'MP': 'MP',
    '% Critical': 'Critical Hits',
    'Agility': 'Agility',
    'Strength': 'Strength',
    'Neutral Damage': 'Neutral Damage',
    'Earth Damage': 'Earth Damage',
    'Intelligence': 'Intelligence',
    'Fire Damage': 'Fire Damage',
    'Air Damage': 'Air Damage',
    'Chance': 'Chance',
    'Water Damage': 'Water Damage',
    'Vitality': 'Vitality',
    'Initiative': 'Initiative',
    'Summons': 'Summon',
    'Range': 'Range',
    'Wisdom': 'Wisdom',
    'Neutral Resistance': 'Neutral Resist',
    'Water Resistance': 'Water Resist',
    'Air Resistance': 'Air Resist',
    'Fire Resistance': 'Fire Resist',
    'Earth Resistance': 'Earth Resist',
    '% Neutral Resistance': '% Neutral Resist',
    '% Air Resistance': '% Air Resist',
    '% Fire Resistance': '% Fire Resist',
    '% Water Resistance': '% Water Resist',
    '% Earth Resistance': '% Earth Resist',
    'Neutral Resistance in PvP': 'Neutral Resist in PVP',
    'Water Resistance in PvP': 'Water Resist in PVP',
    'Air Resistance in PvP': 'Air Resist in PVP',
    'Fire Resistance in PvP': 'Fire Resist in PVP',
    'Earth Resistance in PvP': 'Earth Resist in PVP',
    '% Neutral Resistance in PvP': '% Neutral Resist in PVP',
    '% Air Resistance in PvP': '% Air Resist in PVP',
    '% Fire Resistance in PvP': '% Fire Resist in PVP',
    '% Water Resistance in PvP': '% Water Resist in PVP',
    '% Earth Resistance in PvP': '% Earth Resist in PVP',
    'Prospecting': 'Prospecting',
    'pods': 'Pods',
    'AP Reduction': 'AP Reduction',
    'MP Reduction': 'MP Reduction',
    'Lock': 'Lock',
    'Dodge': 'Dodge',
    'Reflects': 'Reflects',
    'Reflects ': 'Reflects',
    'Reflects  damage': 'Reflects',
    'Pushback Damage': 'Pushback Damage',
    'Trap Damage': 'Trap Damage',
    'Power (traps)': '% Trap Damage',
    'Critical Resistance': 'Critical Resist',
    'Pushback Resistance': 'Pushback Resist',
    'MP Loss Resistance': 'MP Loss Resist',
    'AP Loss Resistance': 'AP Loss Resist',
    'Critical Damage': 'Critical Damage',
    'HP': 'HP',
    'MP Dodge': 'MP Loss Resist',
    '% Air Resist in PVP': '% Air Resist in PVP',
    '% Water Resist in PVP': '% Water Resist in PVP',
    'Fire Resist in PVP': 'Fire Resist in PVP',
    '% Melee Resistance': '% Melee Resist',
    '% Ranged Resistance': '% Ranged Resist',
    'AP Dodge': 'AP Loss Resist',
    '% Melee Damage': '% Melee Damage',
    '% Ranged Damage': '% Ranged Damage',
    '% Weapon Damage': '% Weapon Damage',
    '% Spell Damage': '% Spell Damage',
}

LANGUAGES = ['en', 'fr', 'es', 'pt', 'de', 'it']

# Function to load data for each language
def load_data_for_language(lang, data_type):
    with open(f'all_{data_type}_{lang}.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    
# Load equipment data for all languages
equipment_data = {lang: load_data_for_language(lang, 'equipment') for lang in LANGUAGES}

mount_data = {lang: load_data_for_language(lang, 'mounts') for lang in LANGUAGES}

set_data = {lang: load_data_for_language(lang, 'sets') for lang in LANGUAGES}

# Create a list to store the new formatted items
new_data = []

for item in equipment_data['en']['items']:
    if 'Certificate' in item['type']['name'] or 'Sidekick' in item['type']['name'] or 'Badge' in item['type']['name'] or '[!] [UNKNOWN_TEXT_ID_0]' in item['name'] or 'Perceptor' in item['type']['name']:
        continue
    transformed_item = {}
    if "ankama_id" in item:
        transformed_item["ankama_id"] = item["ankama_id"]
    transformed_item["ankama_type"] = "equipment"
    if "name" in item:
        for lang in LANGUAGES:
            lang_name_key = f"name_{lang}"
            lang_item = next((i for i in equipment_data[lang]['items'] if i['ankama_id'] == item['ankama_id']), None)
            transformed_item[lang_name_key] = lang_item['name'] if lang_item else None
    if "type" in item:
        transformed_item["w_type"] = item["type"]["name"]
    if "level" in item:
        transformed_item["level"] = item["level"]
    if "dofustouch" in item:
        transformed_item["dofustouch"] = item["dofustouch"]
    if "ap_cost" in item:
        transformed_item["ap"] = item["ap_cost"]
    if "max_cast_per_turn" in item:
        transformed_item["uses_per_turn"] = item["max_cast_per_turn"]
    if "range" in item:
        transformed_item["range"] = [item["range"]["min"], item["range"]["max"]]
    if "critical_hit_probability" in item:
        transformed_item["crit_chance"] = item["critical_hit_probability"]
    if "critical_hit_bonus" in item:
        transformed_item["crit_bonus"] = item["critical_hit_bonus"]
    if "conditions" in item:
        transformed_item["conditions"] = [f"{cond['element']['name']} {cond['operator']} {cond['int_value']}" for cond in item["conditions"]]
    if "effects" in item:
        transformed_item["stats"] = [
            [
                eff["int_minimum"] if not eff["ignore_int_min"] else None,
                eff["int_maximum"] if not eff["ignore_int_max"] else None,
                eff["type"]["name"]
            ] for eff in item["effects"]
        ]
        for eff in item["effects"]:
            if eff["type"]["name"] == '-special spell-':
                special_spell_effects = [eff for eff in item.get('effects', []) if eff['type']['name'] == '-special spell-']
                for eff in special_spell_effects:
                    # Add special spell descriptions in different languages
                    for lang in LANGUAGES:
                        lang_item = next((i for i in equipment_data[lang]['items'] if i['ankama_id'] == item['ankama_id']), None)
                        if lang_item:
                            lang_special_spell = next((e['formatted'] for e in lang_item.get('effects', []) if e['type']['name'] == '-special spell-'), None)
                            if lang_special_spell:
                                transformed_item[f"special_spell_{lang}"] = lang_special_spell
    else:
        transformed_item["stats"] = []
    if "conditions" in item:
        transformed_item["has_conditions"] = bool(item["conditions"])
    if "image_urls" in item:
        transformed_item["image_url"] = item["image_urls"]["sd"]
    transformed_item["dofustouch"] = False

    new_data.append(transformed_item)

for item in mount_data['en']['mounts']:
    transformed_item = {}
    transformed_item["dofustouch"] = False
    if "ankama_id" in item:
        transformed_item["ankama_id"] = item["ankama_id"]
    transformed_item["ankama_type"] = "mounts"
    if "name" in item:
        for lang in LANGUAGES:
            lang_name_key = f"name_{lang}"
            lang_item = next((i for i in mount_data[lang]['mounts'] if i['ankama_id'] == item['ankama_id']), None)
            transformed_item[lang_name_key] = lang_item['name'] if lang_item else None
    transformed_item["w_type"] = "Pet"
    transformed_item["level"] = 60
    if "dofustouch" in item:
        transformed_item["dofustouch"] = item["dofustouch"]
    if "conditions" in item:
        transformed_item["conditions"] = [f"{cond['element']['name']} {cond['operator']} {cond['int_value']}" for cond in item["conditions"]]
    if "effects" in item:
        transformed_item["stats"] = [
            [
                eff["int_minimum"] if not eff["ignore_int_min"] else None,
                eff["int_maximum"] if not eff["ignore_int_max"] else None,
                eff["type"]["name"]
            ] for eff in item["effects"]
        ]
    else:
        transformed_item["stats"] = []
    if "conditions" in item:
        transformed_item["has_conditions"] = bool(item["conditions"])
    if "image_urls" in item:
        transformed_item["image_url"] = item["image_urls"]["sd"]

    new_data.append(transformed_item)

for item in new_data:
    if "stats" in item:
        for stat in item["stats"]:
            original_stat_name = stat[-1]  # The original name is the last element in the stat list
            translated_stat_name = STAT_TRANSLATE.get(original_stat_name, original_stat_name)  # Translate or keep as-is
            stat[-1] = translated_stat_name  # Update the name in the stat list

# Write the new JSON file
with open('transformed_equipment.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

new_data = []

for item in set_data['en']["sets"]:

    if "effects" in item:
        for effect_group in item["effects"]:  # Iterate over each group of effects
            for effect in effect_group:  # Iterate over each effect in the group
                if "type" in effect and "name" in effect["type"]:
                    original_type_name = effect["type"]["name"]  # The original name in the type
                    translated_type_name = STAT_TRANSLATE.get(original_type_name, original_type_name)  # Translate or keep as-is
                    effect["type"]["name"] = translated_type_name  # Update the name in the type

    transformed_item = {}
    if "ankama_id" in item:
        transformed_item["ankama_id"] = item["ankama_id"]
    if "name" in item:
        for lang in LANGUAGES:
            lang_name_key = f"name_{lang}"
            lang_item = next((i for i in set_data[lang]['sets'] if i['ankama_id'] == item['ankama_id']), None)
            transformed_item[lang_name_key] = lang_item['name'] if lang_item else None
    if "items" in item:
        transformed_item["items"] = item["items"]
    if "effects" in item:
        transformed_item["stats"] = []
        for i, effect_group in enumerate(item["effects"]):  # Iterate over each group of effects
            transformed_item["stats"].append([
            [
                eff["int_minimum"] if not eff["ignore_int_min"] else None,
                eff["int_maximum"] if not eff["ignore_int_max"] else None,
                eff["type"]["name"] 
            ] for eff in effect_group
        ])
    if "equipment_ids" in item:
        transformed_item["equipment_ids"] = item["equipment_ids"]

    new_data.append(transformed_item)            

# Write the new JSON file
with open('transformed_sets.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)