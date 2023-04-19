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

from chardata.stats_weights import get_stats_weights, set_stats_weights
from chardata.util import set_response, safe_int, get_char_or_raise, HttpResponseJson
from fashionistapulp.structure import get_structure


def stats(request, char_id):
    char = get_char_or_raise(request, char_id)
        
    return set_response(request,
                        'chardata/stats.html',
                        {'char_id': char_id,
                         'advanced': True,
                         'default_weights_json': json.dumps(get_stats_weights(char))},
                        char)


def stats_post(request, char_id):
    char = get_char_or_raise(request, char_id)

    stats_weight = {}
    for stat in get_structure().get_stats_list():
        stats_weight[stat.key] = safe_int(request.POST.get('weight_%s' % stat.key, 0), 0)
    set_stats_weights(char, stats_weight)
    
    return HttpResponseJson(json.dumps(get_stats_weights(char)))

