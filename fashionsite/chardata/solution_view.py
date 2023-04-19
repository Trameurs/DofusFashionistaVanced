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

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
import json

from chardata.encoded_char_id import encode_char_id
from chardata.fashion_action import fashion, get_options
from chardata.lock_forbid import (set_excluded,
                                  set_item_included,
    get_all_inclusions_en_names, get_all_exclusions_en_names)
from chardata.models import Char
import chardata.smart_build
from chardata.solution import get_solution, set_minimal_solution
from chardata.solution_result import SolutionResult
from chardata.util import set_response, get_char_or_raise, get_alias, get_char_encoded_or_raise, \
    HttpResponseText, get_base_stats_by_attr
from fashionistapulp.dofus_constants import SLOTS

from static_s3.templatetags.static_s3 import static
from fashionistapulp.structure import get_structure
from fashionistapulp.modelresult import ModelResultMinimal
from chardata.themes import get_ajax_loader_URL, get_external_image_URL


def solution(request, char_id, empty=False):
    char = get_char_or_raise(request, char_id)
    solution = get_solution(char)
    if solution is None:
        if not empty:
            return fashion(request, char_id)
        else:
            input_ = {}
            input_['options'] = get_options(request, char_id)
            input_['base_stats_by_attr'] = get_base_stats_by_attr(request, char_id)
            input_['char_level'] = char.level
            set_minimal_solution(char, ModelResultMinimal.generate_empty_solution(input_))
    return _solution(request, char_id, False)
    
def _solution(request, char_id, is_guest, encoded_char_id=None):
    char = get_object_or_404(Char, pk=char_id)
    
    inclusions = get_all_inclusions_en_names(char)
    exclusions = get_all_exclusions_en_names(char)
    
    solution = get_solution(char)
    solution_result = SolutionResult(solution,
                                     inclusions,
                                     exclusions)
    params = {'char_id': char_id,
              'lock_item': static('chardata/lock-icon.png'),
              'switch_item': static('chardata/1412645636_Left-right.png'),
              'delete_item': static('chardata/delete-icon.png'),
              'add_item': static('chardata/add-icon.png'),
              'ajax_loader': json.dumps(get_ajax_loader_URL(request)),
              'link_external_image': json.dumps(get_external_image_URL(request)),
              'is_guest': is_guest,
              'is_guest_json': json.dumps(is_guest),
              'encoded_char_id': encoded_char_id,
              'link_shared': char.link_shared,
              'owner_alias': get_alias(char.owner),
              'is_dueler': chardata.smart_build.char_has_aspect(char, 'duel')}
              
    if char.link_shared:
        params['initial_link'] = generate_link(char)

    params.update(solution_result.get_params())

    response = set_response(request, 
                            'chardata/solution.html',
                            params, 
                            char)
    return response


def get_sharing_link(request, char_id):
    char = get_char_or_raise(request, char_id)

    char.link_shared = True
    char.save()
    
    return HttpResponseText(generate_link(char))

def hide_sharing_link(request, char_id):
    char = get_char_or_raise(request, char_id)

    char.link_shared = False
    char.save()
        
    return HttpResponseText('hid')

def solution_linked(request, char_name, encoded_char_id):
    char = get_char_encoded_or_raise(encoded_char_id)
    
    return _solution(request, char.pk, True, encoded_char_id)

def generate_link(char):
    encoded_id = encode_char_id(int(char.id))
    char_name = char.char_name or 'shared'
    return ('https://dofusfashionista.com'
            + reverse('chardata.solution_view.solution_linked',
                      args=(char_name, encoded_id)))

def set_item_locked(request, char_id):
    char = get_char_or_raise(request, char_id)
        
    slot = request.POST.get('slot', None)
    item_name = request.POST.get('equip', None)
    locked = request.POST.get('locked', None)
    
    
    assert slot in SLOTS
    
    structure = get_structure()
    item = structure.get_item_by_name(item_name)
    if item is None:
        or_item = structure.get_or_item_by_name(item_name)
        item_id = or_item[0].id
    else:
        item_id = structure.get_item_by_name(item_name).id
    if locked == 'true':
        set_item_included(char, item_id, slot, True)
    elif locked == 'false':
        set_item_included(char, item_id, slot, False)
    
    return HttpResponseText('char_id %s, slot %s, equip %s, locked %s'
            % (char_id, slot, item_name, str(locked)))

def set_item_forbidden(request, char_id):
    char = get_char_or_raise(request, char_id)
        
    slot = request.POST.get('slot', None)
    item_name = request.POST.get('equip', None)
    forbidden = request.POST.get('forbidden', None)
    
    structure = get_structure()
    item = structure.get_item_by_name(item_name)
    if item is None:
        or_item = structure.get_or_item_by_name(item_name)
        item_id = or_item[0].id
    else:
        item_id = structure.get_item_by_name(item_name).id
    
    if forbidden == 'true':
        set_excluded(char, item_id, True)
    elif forbidden == 'false':
        set_excluded(char, item_id, False)

    return HttpResponseText('char_id %s, slot %s, equip %s, forbidden %s'
            % (char_id, slot, item_name, str(forbidden)))
