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

from django.urls import reverse
from django.db.models import Q
from django.utils.translation import gettext as _
import json

from chardata.models import Char
from chardata.util import set_response
from chardata.encoded_char_id import encode_char_id
from chardata.solution import get_solution
from chardata.solution_result import SolutionResult
from chardata.smart_build import ASPECT_TO_NAME, ASPECT_TO_SHORT_NAME

# Create reverse mapping from short names to keys
SHORT_NAME_TO_KEY = {v: k for k, v in ASPECT_TO_SHORT_NAME.items()}

def translate_build_name(build_name):
    """Translate a build name that may contain multiple aspects separated by / or spaces"""
    if not build_name:
        return ''
    
    # First, try to match the entire string (e.g., "Glass Cannon" as a whole)
    lookup_key = SHORT_NAME_TO_KEY.get(build_name, build_name.lower())
    if lookup_key in ASPECT_TO_NAME:
        return str(ASPECT_TO_NAME[lookup_key])
    
    # Handle slash-separated parts first (e.g., "Agi Glass Cannon/Pushback")
    if '/' in build_name:
        parts = build_name.split('/')
        translated_parts = []
        for part in parts:
            part = part.strip()
            if part:
                # Recursively translate each part (which may contain spaces)
                translated_parts.append(translate_build_name(part))
        return '/'.join(translated_parts)
    
    # Handle space-separated parts (e.g., "Int Crit Glass Cannon")
    # But we need to be smart about multi-word build types like "Glass Cannon"
    if ' ' in build_name:
        # Try to find multi-word matches first (longer matches first)
        words = build_name.split(' ')
        translated_parts = []
        i = 0
        while i < len(words):
            # Try matching 2 words first (for "Glass Cannon", etc.)
            matched = False
            if i + 1 < len(words):
                two_word = f"{words[i]} {words[i+1]}"
                lookup_key = SHORT_NAME_TO_KEY.get(two_word, two_word.lower())
                if lookup_key in ASPECT_TO_NAME:
                    translated_parts.append(str(ASPECT_TO_NAME[lookup_key]))
                    i += 2
                    matched = True
            
            # If no 2-word match, try single word
            if not matched:
                lookup_key = SHORT_NAME_TO_KEY.get(words[i], words[i].lower())
                translated_parts.append(str(ASPECT_TO_NAME.get(lookup_key, words[i])))
                i += 1
        
        return ' '.join(translated_parts)
    
    # Single word that wasn't found
    return build_name

def shared_builds(request):
    """Display a page with all shared builds, with search and filter options."""
    
    # Get filter parameters from GET request
    char_class = request.GET.get('char_class', '')
    min_level = request.GET.get('min_level', '')
    max_level = request.GET.get('max_level', '')
    order_by = request.GET.get('order_by', 'created')  # views, modified, created (default: created)
    search_query = request.GET.get('search', '')
    
    # Get selected build aspects from checkboxes
    selected_aspects = []
    for aspect in ['str', 'int', 'cha', 'agi', 'omni', 'vit', 'res', 'wis', 
                   'glasscannon', 'dam', 'crit', 'noncrit', 'heal', 'aprape', 'mprape',
                   'pvp', 'duel', 'trap', 'summon', 'pushback', 'pp', 'pods', 'balanced']:
        if request.GET.get(f'check_{aspect}'):
            selected_aspects.append(aspect)
    
    # Start with all shared, non-deleted builds
    builds = Char.objects.filter(link_shared=True, deleted=False)
    
    # Apply filters
    if char_class:
        builds = builds.filter(char_class=char_class)
    
    # Filter by selected build aspects (if any)
    if selected_aspects:
        # Special handling for Balanced: if Balanced is selected, we need to filter differently
        # because balanced builds don't have focus aspects stored in char_build
        if 'balanced' in selected_aspects:
            # Get all the focus aspects that should NOT be in the build
            focus_aspects = ['vit', 'glasscannon', 'dam', 'heal', 'aprape', 'mprape', 
                           'crit', 'res', 'wis', 'pp', 'pods', 'trap', 'summon', 
                           'pushback', 'noncrit']
            
            # Remove balanced from the list and filter for other aspects normally
            aspects_to_filter = [aspect for aspect in selected_aspects if aspect != 'balanced']
            
            # Match builds that contain the selected non-balanced aspects
            for aspect in aspects_to_filter:
                aspect_short = ASPECT_TO_SHORT_NAME.get(aspect, aspect)
                builds = builds.filter(char_build__icontains=aspect_short)
            
            # Exclude builds that contain any focus aspect (these are not balanced)
            for focus_aspect in focus_aspects:
                focus_short = ASPECT_TO_SHORT_NAME.get(focus_aspect, focus_aspect)
                builds = builds.exclude(char_build__icontains=focus_short)
        else:
            # Special handling for Omni: if Omni is selected, only search for Omni builds
            # even if individual elements are also checked (for UI purposes)
            if 'omni' in selected_aspects:
                # Filter only for Omni, ignore individual element selections
                aspects_to_filter = [aspect for aspect in selected_aspects 
                                   if aspect not in ['str', 'int', 'cha', 'agi']]
            else:
                aspects_to_filter = selected_aspects
            
            # Match builds that contain ALL selected aspects
            for aspect in aspects_to_filter:
                # Map aspect keys to their short names for matching
                aspect_short = ASPECT_TO_SHORT_NAME.get(aspect, aspect)
                builds = builds.filter(char_build__icontains=aspect_short)
    
    if min_level:
        try:
            builds = builds.filter(level__gte=int(min_level))
        except ValueError:
            pass
    
    if max_level:
        try:
            builds = builds.filter(level__lte=int(max_level))
        except ValueError:
            pass
    
    if search_query:
        builds = builds.filter(
            Q(name__icontains=search_query) | 
            Q(char_name__icontains=search_query)
        )
    
    # Order results
    if order_by == 'views':
        builds = builds.order_by('-view_count', '-modified_time')
    elif order_by == 'modified':
        builds = builds.order_by('-modified_time')
    elif order_by == 'created':
        builds = builds.order_by('-created_time')
    else:
        builds = builds.order_by('-view_count', '-modified_time')
    
    # Limit to first 100 results for performance
    builds = builds[:100]
    
    # Prepare build data with links and stats
    builds_data = []
    for char in builds:
        encoded_id = encode_char_id(int(char.id))
        char_name = char.char_name or 'shared'
        link = 'https://fashionistavanced.com' + reverse('solution_linked',
                                                          args=(char_name, encoded_id))
        
        # Try to get solution stats if available
        solution = get_solution(char)
        total_stats = None
        if solution:
            try:
                sol_result = SolutionResult(solution)
                stats = sol_result.get_stats()
                if stats:
                    # Calculate a simple "score" based on total stats
                    total_stats = sum([v for v in stats.values() if isinstance(v, (int, float)) and v > 0])
            except:
                pass
        
        # Translate build type name if available
        # Check if build has no focus aspects (which means it's balanced)
        focus_aspects = ['Vit', 'Glass Cannon', 'Dam', 'Heals', 'AP Red', 'MP Red', 
                        'Crit', 'Res', 'Leecher', 'PP', 'Pods', 'Traps', 'Summons', 
                        'Pushback', 'Non-Crit']
        
        has_focus = any(focus in char.char_build for focus in focus_aspects if char.char_build)
        
        if char.char_build and not has_focus:
            # Build has elements but no focus = balanced
            build_name_translated = f"{translate_build_name(char.char_build)} {ASPECT_TO_NAME['balanced']}"
        elif not char.char_build:
            # No build type at all = balanced
            build_name_translated = str(ASPECT_TO_NAME['balanced'])
        else:
            build_name_translated = translate_build_name(char.char_build)
        
        builds_data.append({
            'char': char,
            'link': link,
            'total_stats': total_stats or 0,
            'view_count': char.view_count,
            'build_name_translated': build_name_translated,
        })
    
    # Get all unique classes for filter dropdown
    all_classes = Char.objects.filter(link_shared=True, deleted=False).values_list('char_class', flat=True).distinct().order_by('char_class')
    
    # Prepare aspect names and layout for checkboxes (same as projdetails.html)
    aspect_to_name = {k: str(v) for k, v in ASPECT_TO_NAME.items()}
    aspect_layout = [['str', 'int', 'cha', 'agi', 'omni'],
                     ['pvp', 'duel'],
                     ['balanced', 'vit', 'glasscannon', 'dam', 'heal', 'aprape', 'mprape', 'crit'],
                     ['res', 'wis', 'pp', 'pods', 'trap', 'summon', 'pushback', 'noncrit']]
    
    params = {
        'builds': builds_data,
        'all_classes': all_classes,
        'aspect_to_name': json.dumps(aspect_to_name),
        'aspect_layout': json.dumps(aspect_layout),
        'selected_aspects': json.dumps(selected_aspects),
        'filters': {
            'char_class': char_class,
            'min_level': min_level,
            'max_level': max_level,
            'order_by': order_by,
            'search': search_query,
        }
    }
    
    response = set_response(request, 
                            'chardata/shared_builds.html',
                            params)
    return response
