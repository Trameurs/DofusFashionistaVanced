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
from itemscraper.items import ItemscraperItem

class ExampleSpider(scrapy.Spider):
    name = "itemspider"
    allowed_domains = ["dofus.com"]
    start_urls = (
        'http://www.dofus.com/en/mmorpg/encyclopedia/equipment/14077-count-harebourg-ring',
        'http://www.dofus.com/en/mmorpg/encyclopedia/equipment/14091-cycloid-amulet',
    )

    def parse(self, response):
        item_name_node = response.xpath("//div[@class='ak-page-header']/h1/node()")[2]
        item_src_node = response.xpath("//img[@class='img-maxresponsive']/@src")[0]
        item = ItemscraperItem()
        item['name'] = item_name_node.extract().strip()
        item['image_url'] = item_src_node.extract().strip()
        yield item
