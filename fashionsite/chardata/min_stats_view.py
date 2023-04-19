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

from chardata.min_stats import get_min_stats, set_min_stats, convert_dict_index_name_to_key
from chardata.util import set_response, safe_int, get_char_or_raise, HttpResponseJson
from fashionistapulp.dofus_constants import AGI_TARGETS, CRIT_TARGETS,\
    STAT_ORDER
from fashionistapulp.structure import get_structure
from django.utils.translation import ugettext as _

def min_stats(request, char_id):
    char = get_char_or_raise(request, char_id)
        
    initial_data = _get_initial_data(char)
    structure = get_structure()
    
    stats = []
    for stat in structure.get_stats_list():
        stat_to_add = {}
        stat_to_add['key'] = stat.key
        stat_to_add['name'] = _(stat.name)
        stats.append(stat_to_add)
    
    stats = [stat for stat in
        sorted(stats, key=lambda stat: STAT_ORDER[stat['key']])]
    
    fixed_fields = []
    ap = {}
    ap['key'] = 'ap'
    ap['name'] = _('AP')
    fixed_fields.append(ap)
    mp = {}
    mp['key'] = 'mp'
    mp['name'] = _('MP')
    fixed_fields.append(mp)
    rangestat = {}
    rangestat['key'] = 'range'
    rangestat['name'] = _('Range')
    fixed_fields.append(rangestat)
    
    adv_min_fields = structure.get_adv_mins()
    
    return set_response(request,
                        'chardata/min_stats.html',
                        {'advanced': True,
                         'char_id': char_id,
                         'stats_order': json.dumps(stats),
                         'stats_fixed': json.dumps(fixed_fields),
                         'stats_adv': json.dumps(adv_min_fields),
                         'initial_data': json.dumps(initial_data),
                         'crit_targets': CRIT_TARGETS,
                         'agility_targets': AGI_TARGETS},
                        char)


def min_stats_post(request, char_id):
    char = get_char_or_raise(request, char_id)
    structure = get_structure()

    minimum_values = {}
    for stat in get_structure().get_stats_list():
        minimum = safe_int(request.POST.get('min_%s' % stat.key, ''))
        if minimum is not None:
            minimum_values[stat.name] = minimum

    minimum = safe_int(request.POST.get('min_hp'))
    if minimum is not None:
        minimum_values['HP'] = minimum

    adv_stats = structure.get_adv_mins()
    minimum_values['adv_mins'] = {}
    for stat in adv_stats:
        minimum = safe_int(request.POST.get('min_%s' % stat['key'], ''))
        if minimum is not None:
            minimum_values['adv_mins'][stat['name']] = minimum
    set_min_stats(char, minimum_values)        
    
    return HttpResponseJson(json.dumps(_get_initial_data(char)))
    
def _get_initial_data(char):
    mins = get_min_stats(char)
    mins = convert_dict_index_name_to_key(mins)
    structure = get_structure()
        
    for stat in get_structure().get_stats_list():
        if stat.key not in mins:
            mins[stat.key] = ''
    if 'hp' not in mins:
        mins['hp'] = ''
    adv_mins = structure.get_adv_mins()
    if 'adv_mins' not in mins:
        mins['adv_mins'] = {}
    for stat in adv_mins:
        if stat['key'] not in mins['adv_mins']:
            mins['adv_mins'][stat['key']] = ''
    
    return {'minimum_stats': mins}

