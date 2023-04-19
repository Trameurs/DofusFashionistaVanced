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
from urlparse import urljoin
from itemscraper.items import ItemscraperItem

class VenomSpider(scrapy.Spider):
    name = "venom"
    DOWNLOAD_DELAY=1
    allowed_domains = ["dofus.com"]
    start_urls = [
    #    'https://www.dofus.com/en/mmorpg/encyclopedia/equipment?page=%d' % page
    #    for page in range(1, 124 + 1)
    ] + [
        'https://www.dofus.com/en/mmorpg/encyclopedia/weapons?page=%d' % page
        for page in range(1, 40 + 1)
    ] + [
        #'https://www.dofus.com/en/mmorpg/encyclopedia/pets?page=%d' % page
        #for page in range(1, 7 + 1)
    ] + [
        #'https://www.dofus.com/en/mmorpg/encyclopedia/mounts?page=%d' % page
        #for page in range(1, 3 + 1)
    ]

    def parse(self, response):
        item_lines = response.xpath("//tbody/node()")
        for item_line in item_lines:
            href_try = item_line.xpath(".//a/@href")
            if href_try:
                href = href_try[0].extract()
                yield scrapy.Request(urljoin(response.url, href),
                                 callback=self.look_at_item_page)
            
    def look_at_item_page(self, response):
        try_item_name = response.xpath("//h1[@class='ak-return-link']/node()")
        item_name_node = try_item_name[2]
        
        try_item_id = response.xpath("//a[@class='ak-flag-fr']/@href")
        for result in try_item_id:
            try_link = result.extract()
            if try_link:
                find_id = try_link.split('/')
                for s in find_id:
                    if len(s)>0 and s[0].isdigit():
                        find_id = s.split('-')
                        if find_id:
                            ankama_id = int(find_id[0])
                            break
        
        item = ItemscraperItem()
        item['name'] = item_name_node.extract().strip()
        item['ankama_id'] = ankama_id
        yield item
