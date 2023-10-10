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

# Read the original JSON file
with open('all_items.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

# Create a list to store the new formatted items
new_data = []

for item in original_data['items']:
    if 'Certificate' in item['type']['name']:
        continue
    transformed_item = {}
    if "ankama_id" in item:
        transformed_item["ankama_id"] = item["ankama_id"]
    if "name" in item:
        transformed_item["name"] = item["name"]
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
        transformed_item["stats"] = [[eff["int_minimum"], eff["int_maximum"], eff["type"]["name"]] for eff in item["effects"]]
    else:
        transformed_item["stats"] = []
    if "conditions" in item:
        transformed_item["has_conditions"] = bool(item["conditions"])
    if "image_urls" in item:
        transformed_item["image_url"] = item["image_urls"]["sd"]
    transformed_item["dofustouch"] = False

    new_data.append(transformed_item)

with open('all_mounts.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

for item in original_data['mounts']:
    transformed_item = {}
    transformed_item["dofustouch"] = False
    if "ankama_id" in item:
        transformed_item["ankama_id"] = item["ankama_id"]
    if "name" in item:
        transformed_item["name"] = item["name"]
    transformed_item["w_type"] = "Pet"
    transformed_item["level"] = 60
    if "dofustouch" in item:
        transformed_item["dofustouch"] = item["dofustouch"]
    transformed_item["ap"] = 0
    if "conditions" in item:
        transformed_item["conditions"] = [f"{cond['element']['name']} {cond['operator']} {cond['int_value']}" for cond in item["conditions"]]
    if "effects" in item:
        transformed_item["stats"] = [[eff["int_minimum"], eff["int_maximum"], eff["type"]["name"]] for eff in item["effects"]]
    else:
        transformed_item["stats"] = []
    if "conditions" in item:
        transformed_item["has_conditions"] = bool(item["conditions"])
    if "image_urls" in item:
        transformed_item["image_url"] = item["image_urls"]["sd"]

    new_data.append(transformed_item)

# Write the new JSON file
with open('transformed_items.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)