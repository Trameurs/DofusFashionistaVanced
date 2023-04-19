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
from fashionistapulp.structure import get_structure
from itemscraper.items import ItemscraperItemCondition

IDS = []
structure = get_structure()
a = 0
for item in structure.get_available_items_list():
    if item.type != structure.get_type_id_by_name('Pet'):
        ankama_id = item.ankama_id
        if ankama_id:
            IDS.append(ankama_id)

START_URLS = ['https://www.dofus.com/en/mmorpg/encyclopedia/equipment/%d-x' % page_id
              for page_id in IDS]

class RosettaSpider(scrapy.Spider):
    name = "find_conds"
    download_delay=1.5
    allowed_domains = ["dofus-touch.com"]
    start_urls = START_URLS

    def parse(self, response):
        try_item_name = response.xpath("//h1[@class='ak-return-link']/node()")
        item_name_node = try_item_name[2]
        
        try_item_name = response.xpath("//div[@class='ak-panel-title']/node()")
        #with open('has_conditions.txt', 'a') as f:
        for thingy in try_item_name:
            if "Conditions" in thingy.extract():
                #f.write(item_name + '\n')
                try_item_condition = response.xpath("//div[@class='ak-title']/node()")
                item = ItemscraperItemCondition()
                item['name'] = item_name_node.extract().strip()
                item['condition'] = "Not found"
                for content in try_item_condition:
                    if " > " in content.extract() or " < " in content.extract(): 
                        item['condition'] = content.extract().strip()
                yield item