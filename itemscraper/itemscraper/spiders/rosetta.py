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

import scrapy
from itemscraper.items import ItemscraperTranslatedItem
from scrapy import Request
from fashionistapulp.structure import get_structure

MODE = 'equip'
#SECTION = 0

BASE_URLS_EN = {
    'mounts': 'https://www.dofus.com/en/mmorpg/encyclopedia/mounts/%d-x',
    'equip': 'https://www.dofus.com/en/mmorpg/encyclopedia/equipment/%d-x',
    'set': 'https://www.dofus.com/en/mmorpg/encyclopedia/sets/%d-x',
}
BASE_URLS = {
    'mounts': [
        'https://www.dofus.com/pt/mmorpg/enciclopedia/montarias/%d-x',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/montures/%d-x',
        'https://www.dofus.com/de/mmorpg/leitfaden/reittiere/%d-x',
        'https://www.dofus.com/es/mmorpg/enciclopedia/monturas/%d-x',
        'https://www.dofus.com/it/mmorpg/enciclopedia/cavalcature/%d-x',
    ],
    'equip': [
        'https://www.dofus.com/pt/mmorpg/enciclopedia/equipamentos/%d-x',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/%d-x',
        'https://www.dofus.com/de/mmorpg/leitfaden/ausruestung/%d-x',
        'https://www.dofus.com/es/mmorpg/enciclopedia/equipos/%d-x',
        'https://www.dofus.com/it/mmorpg/enciclopedia/equipaggiamenti/%d-x',
    ],
    'set': [
        'https://www.dofus.com/pt/mmorpg/enciclopedia/conjuntos/%d-x',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/panoplies/%d-x',
        'https://www.dofus.com/de/mmorpg/leitfaden/sets/%d-x',
        'https://www.dofus.com/es/mmorpg/enciclopedia/sets/%d-x',
        'https://www.dofus.com/it/mmorpg/enciclopedia/panoplie/%d-x',
    ],
}
# START = {
#     'mounts': 1,
#     #'equip': 1 + 1000 * SECTION,
#     'equip': 16000,
#     'set': 1,
# }
# LIMIT = {
#     'mounts': 100,
#     #'equip': 1000,
#     'equip': 2000,
#     'set': 400,
# }

IDS = {}
IDS['equip'] = []
IDS['set'] = []
structure = get_structure()
a = 0
for item in structure.get_available_items_list():
    if item.type != structure.get_type_id_by_name('Pet'):
        ankama_id = item.ankama_id
        if ankama_id:
            IDS['equip'].append(ankama_id)
for each_set in structure.get_sets_list():
    ankama_id = each_set.ankama_id
    if ankama_id:
        IDS['set'].append(ankama_id)
        


# START_URLS = [BASE_URLS_EN[MODE] % page_id
#               for page_id in range(START[MODE], LIMIT[MODE] + START[MODE])]

START_URLS = [BASE_URLS_EN[MODE] % page_id
              for page_id in IDS[MODE]]

class RosettaSpider(scrapy.Spider):
    name = "rosetta"
    download_delay=1
    allowed_domains = ["dofus.com"]
    start_urls = START_URLS

    def parse(self, response):
        title = response.xpath('//title/node()')[0].extract().strip()
        url = response.request.url
        reverse_id = int(url.split('/')[-1].split('-')[0])
        
        item = ItemscraperTranslatedItem()
        item['url'] = url
        item['localized_name'] = title.split(' - ')[0]
        yield item
        if '/en/' in response.request.url:
            for base_url in BASE_URLS[MODE]:
                yield Request(base_url % reverse_id, callback = self.parse)
