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
from itemscraper.items import MissingNo, ItemscraperTouchSetData

UNDER_100_IDS = range(1, 501)



BASE_URL = 'https://www.dofus-touch.com/en/mmorpg/encyclopedia/sets/%d-ourobubble-set'
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

START_URLS = [BASE_URL % item_id for item_id in UNDER_100_IDS]

class TrapDoorSpider(scrapy.Spider):
    name = "touch_set_bonus_scraper"
    download_delay=1
    allowed_domains = ["dofus.com"]
    start_urls = START_URLS
    handle_httpstatus_list = [404]

    def parse(self, response):
        if response.status == 404:
            item = MissingNo()
            item['ankama_id'] = response.request.url.split('/')[-1]
            item['ankama_id'] = int(item['ankama_id'].split('-')[0])
            item['removed'] = True
            yield item
            return
        
        set_data = ItemscraperTouchSetData()
        item = MissingNo()
        item['ankama_id'] = response.request.url.split('/')[-1]
        item['ankama_id'] = int(item['ankama_id'].split('-')[0])
        print item['ankama_id'] #this part works

        e = response.xpath('//div[@class=\'ak-main-page\']')
        e = e.xpath('//div[@class=\'ak-title-container ak-backlink\']')

        set_name = e.xpath('.//h1[@class=\'ak-return-link\']/text()')[1].extract().strip()
        set_data['name'] = set_name
        set_data['ankama_id'] = item['ankama_id']
        print set_name
        
        item_list = []
        i = 0
        for result in response.xpath('.//td[@class=\'ak-set-composition-name\']'):
            i = i + 1
            print '%d' %i
            item_name = result.xpath('.//a/text()')[0].extract().strip()
            print item_name
            item_list.append(item_name)
        set_data['items'] = item_list
        
        bonus_dict = {}
        for i in range(1, 9):
            bonus_list = []
            e_string = '//div[@class=\'set-bonus-list set-bonus-%d\']//div[@class=\'ak-title\']' %i
            f = e.xpath(e_string)
            for bonus in f:
                stat = bonus.extract().replace("\n", "")
                stat = stat.split('<')[1]
                stat = stat.split('>')[1]
                stat = stat.strip()
                bonus_list.append(stat)
            if len(bonus_list) > 0:
                list_name = 'bonus_%d' %i
                bonus_dict[list_name] = bonus_list
        set_data['bonus'] = bonus_dict
            
        

        yield set_data
