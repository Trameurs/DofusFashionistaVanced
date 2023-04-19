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

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItemscraperItem(scrapy.Item):
    name = scrapy.Field()
    ankama_id = scrapy.Field()

class ItemscraperItemTouch(scrapy.Item):
    name = scrapy.Field()
    ankama_id = scrapy.Field()
    
class ItemscraperItemCondition(scrapy.Item):
    name = scrapy.Field()
    condition = scrapy.Field()

class ItemscraperTranslatedItem(scrapy.Item):
    url = scrapy.Field()
    localized_name = scrapy.Field()
    
class ItemscraperTranslatedSet(scrapy.Item):
    lang = scrapy.Field()
    localized_name = scrapy.Field()


class ItemscraperWeaponData(scrapy.Item):
    ankama_id = scrapy.Field()
    ap = scrapy.Field()
    uses_per_turn = scrapy.Field()
    range = scrapy.Field()
    crit_chance = scrapy.Field()
    crit_bonus = scrapy.Field()
    name = scrapy.Field()
    w_type = scrapy.Field()
    level = scrapy.Field()
    stats = scrapy.Field()
    dofustouch = scrapy.Field()
    conditions = scrapy.Field()
    has_conditions = scrapy.Field()
    
class ItemscraperClassItemData(scrapy.Item):
    ankama_id = scrapy.Field()
    name = scrapy.Field()
    level = scrapy.Field()
    w_type = scrapy.Field()
    extra_lines = scrapy.Field()
    lang = scrapy.Field()
    
class MissingNo(scrapy.Item):
    ankama_id = scrapy.Field()
    removed = scrapy.Field()
    
class ItemscraperSetData(scrapy.Item):
    ankama_id = scrapy.Field()
    name = scrapy.Field()
    bonus = scrapy.Field()
    
class ItemscraperTouchSetData(scrapy.Item):
    ankama_id = scrapy.Field()
    name = scrapy.Field()
    bonus = scrapy.Field()
    items = scrapy.Field()
