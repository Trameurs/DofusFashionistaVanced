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

from django.utils.translation import get_language
import re


BASE_URLS = {
    'en': 'https://www.dofus.com/en/mmorpg/encyclopedia/%s/%d-%s',
    'fr': 'https://www.dofus.com/fr/mmorpg/encyclopedie/%s/%d-%s',
    'pt': 'https://www.dofus.com/pt/mmorpg/enciclopedia/%s/%d-%s',
    'es': 'https://www.dofus.com/es/mmorpg/enciclopedia/%s/%d-%s',
    'de': 'https://www.dofus.com/de/mmorpg/leitfaden/%s/%d-%s',
    'it': 'https://www.dofus.com/it/mmorpg/enciclopedia/%s/%d-%s',
}

ANKAMA_TYPE_TO_SITE_CATEGORY = {
    'en': {'pet': 'pets',
           'mounts': 'mounts',
           'equipment': 'equipment'},
    'fr': {'pet': 'familiers',
           'mounts': 'montures',
           'equipment': 'equipements'},
    'pt': {'pet': 'mascotes',
           'mounts': 'montarias',
           'equipment': 'equipamentos'},
    'es': {'pet': 'mascotas',
           'mounts': 'monturas',
           'equipment': 'equipos'},
    'de': {'pet': 'vertraute',
           'mounts': 'reittiere',
           'equipment': 'ausruestung'},
    'it': {'pet': 'famigli',
           'mounts': 'cavalcature',
           'equipment': 'equipaggiamenti'}
}

def get_item_link(ankama_type, ankama_id, name):
    if not ankama_id or not ankama_type:
        return None

    name = name.strip().lower()
    name = name.replace('\'s', '')
    name = name.replace(' ', '-')
    regex = re.compile('[^a-zA-Z-]')
    name = regex.sub('', name)

    lang = get_language()
    return (BASE_URLS[lang]
            % (ANKAMA_TYPE_TO_SITE_CATEGORY[lang][ankama_type], ankama_id, name))
