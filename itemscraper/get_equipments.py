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

import requests
import json

# API endpoint
api_endpoint = "https://api.dofusdu.de/dofus2/en/items/equipment/all"
api_endpoint_mount = "https://api.dofusdu.de/dofus2/en/mounts/all"
api_endpoint_sets = "https://api.dofusdu.de/dofus2/en/sets/all"

# Make the GET request
response = requests.get(api_endpoint)

# Check for successful request
if response.status_code == 200:
    json_data = response.json()

    # Save to a JSON file
    with open('all_items.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print("Successfully saved all items to 'all_items.json'")

else:
    print(f"Failed to retrieve equipment data. Status code: {response.status_code}")

# Make the GET request
response = requests.get(api_endpoint_mount)

# Check for successful request
if response.status_code == 200:
    json_data = response.json()

    # Save to a JSON file
    with open('all_mounts.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print("Successfully saved all mounts to 'all_mounts.json'")

else:
    print(f"Failed to retrieve mounts data. Status code: {response.status_code}")

# Make the GET request
response = requests.get(api_endpoint_sets)

# Check for successful request
if response.status_code == 200:
    json_data = response.json()

    # Save to a JSON file
    with open('all_sets.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print("Successfully saved all sets to 'all_sets.json'")

else:
    print(f"Failed to retrieve sets data. Status code: {response.status_code}")

